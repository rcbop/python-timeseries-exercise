from consumer.bootstrap import bootstrap_di
from consumer.worker import Worker
from kink import inject


@inject
def main(consumer_worker: Worker):
    consumer_worker.run()


if __name__ == "__main__":
    bootstrap_di()
    main()
