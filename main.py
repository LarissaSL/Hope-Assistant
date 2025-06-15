import sys

from HopeInterface import HopeApp

def main():
    print("🚀 Iniciando Hope Assistant...")
    print("=" * 50)

    try:
        app = HopeApp()
        app.run()

    except KeyboardInterrupt:
        print("\n👋 Hope Assistant encerrada pelo usuário")
        return 0

    print("\n👋 Hope Assistant encerrada com sucesso!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)