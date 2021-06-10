"""Main."""

from .Application import Application
import os


def main():
  """Change working directory to project folder and call mainloop."""
  srcDir = os.path.dirname(__file__)
  os.chdir(srcDir)
  Application().mainloop()


if __name__ == "__main__":
  main()
