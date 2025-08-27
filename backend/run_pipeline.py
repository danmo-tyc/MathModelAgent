import argparse
import asyncio
from dotenv import load_dotenv
from app.core.workflow import MathModelWorkFlow
from app.schemas.request import Problem
from app.schemas.enums import CompTemplate, FormatOutPut
from app.utils.common_utils import create_task_id, create_work_dir


async def main(args: argparse.Namespace) -> None:
    """Run the modeling workflow with CLI arguments."""

    # Load environment variables from .env files for API keys, etc.
    load_dotenv()

    if args.question:
        ques_all = args.question
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            ques_all = f.read()
    else:
        raise ValueError("please provide --question or --file")

    task_id = create_task_id()
    create_work_dir(task_id)
    problem = Problem(
        task_id=task_id,
        ques_all=ques_all,
        comp_template=CompTemplate[args.template],
        format_output=FormatOutPut[args.format],
    )
    await MathModelWorkFlow().execute(problem)
    print(f"Task {task_id} finished. Results saved to project/work_dir/{task_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full math modeling pipeline")
    parser.add_argument("--question", type=str, help="Problem statement text")
    parser.add_argument("--file", type=str, help="Path to text file containing problem statement")
    parser.add_argument(
        "--template", type=str, default="CHINA", choices=[e.name for e in CompTemplate]
    )
    parser.add_argument(
        "--format", type=str, default="Markdown", choices=[e.name for e in FormatOutPut]
    )
    return parser.parse_args()


if __name__ == '__main__':
    asyncio.run(main(parse_args()))
