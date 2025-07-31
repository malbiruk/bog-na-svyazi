from datetime import datetime

import pandas as pd
from sentence_transformers import SentenceTransformer, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import InputExample
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from config import initialize_logging

noww = datetime.now().strftime("%d%m%Y_%H%M%S")
logger = initialize_logging(fname="finetuning/finetuning.log")


def train_model(
    model_name: str = "cointegrated/rubert-tiny2",
    trainig_data_path: str = "feedback/feedback.tsv",
    epochs: int = 10,
    batch_size: int = 2,
):
    data = pd.read_csv(trainig_data_path, sep="\t")
    data = data.dropna()

    train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

    train_data["feedback"] = train_data["feedback"].map({"good": 1, "bad": 0})
    val_data["feedback"] = val_data["feedback"].map({"good": 0.95, "bad": 0.55})

    train_examples = [
        InputExample(texts=[row["user_input"], row["quote"]], label=row["feedback"])
        for _, row in train_data.iterrows()
    ]
    model = SentenceTransformer(model_name)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)
    train_loss = losses.ContrastiveLoss(model=model)
    evaluator = EmbeddingSimilarityEvaluator(
        val_data["user_input"].tolist(),
        val_data["quote"].tolist(),
        val_data["feedback"].tolist(),
        batch_size=batch_size,
    )

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        evaluator=evaluator,
        epochs=epochs,
        output_path=f"finetuning/models/rbt2-{noww}",
    )

    base_model = SentenceTransformer(model_name)
    print("Base model:")
    evaluator(base_model)

    print("Finetuned model:")
    evaluator(model)


if __name__ == "__main__":
    logger.info("starting training...")
    train_model()
    logger.info("training complete!")
