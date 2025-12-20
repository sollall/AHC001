from concurrent.futures import ProcessPoolExecutor
import logging
import hydra
from omegaconf import DictConfig

from utils.inout import run_module

logging.basicConfig(level=logging.INFO)

@hydra.main(config_path='./conf', config_name='config', version_base="1.3")
def main(cfg:DictConfig):

    if cfg.general.executor_type=="ProcessPoolExecutor":
        executor_class=ProcessPoolExecutor
    else:
        raise ValueError("Please specify the executor type.")

    total_score,total_time=0,0
    num_tests = cfg.general.num_tests

    with executor_class(max_workers=cfg.general.max_workers) as executor:
        results = executor.map(run_module,
                                [cfg.general.module_name for _ in range(num_tests)],
                                [cfg.optimizer for _ in range(num_tests)],
                                [i for i in range(num_tests)]
                            )
        for result in results:
            score,passed_time=result
            total_score+=score
            total_time+=passed_time

    # Calculate statistics
    avg_score = total_score / num_tests
    avg_time = total_time / num_tests

    logging.info(f"{'='*50}")
    logging.info(f"Results Summary:")
    logging.info(f"  Total Score: {total_score}")
    logging.info(f"  Average Score: {avg_score:.2f}")
    logging.info(f"  Total Time: {total_time:.2f}s")
    logging.info(f"  Average Time: {avg_time:.2f}s")
    logging.info(f"  Test Cases: {num_tests}")
    logging.info(f"{'='*50}")

    return total_score

if __name__ == "__main__":
    main()