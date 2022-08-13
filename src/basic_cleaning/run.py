#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="Performs basic cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info(f"Info: Downloading artifact {args.input_artifact}")
    print("args.input_artifact ",args.input_artifact)
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    print("artifact_local_path ",artifact_local_path)
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])


    logger.info(f"Infor: Saving cleaned data to {args.output_artifact}")
    # save cleaned data
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
                name=args.output_artifact,
                type=args.output_type,
                description=args.output_description,
    )
    artifact.add_file(args.output_artifact)

    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="In this step, we can use to clean the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="artifact input - please sample csv file",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="please give cleane_data.csv",
        required=True
    )


    parser.add_argument(
        "--output_type",
        type=str,
        help="please give type of the output",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="please give your description of the output",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="please give the minimum price to consider filtering the price data",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="please give the maximum price to consider filtering the price data",
        required=True
    )


    args = parser.parse_args()

    go(args)
