
import lxbdocs

if __name__ == "__main__":
    docs = lxbdocs.Docs("../site/src", "../www", "../site/theme", "module")
    docs.make()
