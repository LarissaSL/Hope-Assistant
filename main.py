import sys

from HopeInterface import HopeApp

def main():
    print("Iniciando Hope Assistant...")
    print("=" * 50)

    app = HopeApp()
    app.run()

    print("\n👋 Hope Assistant encerrada com sucesso!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)