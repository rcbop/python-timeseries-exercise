"""generate data."""
import logging

from generator.insert import InsertGenerator
from generator.bootstrap import bootstrap_di

def main():
    InsertGenerator().run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bootstrap_di()
    main()
