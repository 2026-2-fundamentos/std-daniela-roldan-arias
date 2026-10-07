import shutil
import string
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
INPUT_DIR = ACTIVITY_DIR / "temp" / "input"
OUTPUT_DIR = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def main():
    # Crear las carpetas y limpiar los archivos temporales anteriores.
    for folder in (INPUT_DIR, OUTPUT_DIR, SUBMISSION_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    for folder in (INPUT_DIR, OUTPUT_DIR):
        for file in folder.iterdir():
            if file.is_file():
                file.unlink()

    # Generar mil copias de cada archivo original.
    n = 1000
    for file in DATA_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        for i in range(1, n + 1):
            destination = INPUT_DIR / f"{file.stem}_{i:05d}.txt"
            destination.write_text(text, encoding="utf-8")

    # Mapper: emitir (palabra, 1) por cada aparición.
    pairs = []
    punctuation_table = str.maketrans("", "", string.punctuation)
    for file in INPUT_DIR.glob("*.txt"):
        with file.open("r", encoding="utf-8") as source:
            for line in source:
                line = line.lower().translate(punctuation_table)
                for word in line.split():
                    pairs.append((word, 1))

    # Ordenar para juntar las apariciones de cada palabra.
    pairs.sort()

    # Reducer: sumar las apariciones de cada palabra.
    result = []
    for word, count in pairs:
        if result and result[-1][0] == word:
            result[-1] = (word, result[-1][1] + count)
        else:
            result.append((word, count))

    # Escribir los conteos y el marcador de éxito.
    output_file = OUTPUT_DIR / "part-00000"
    with output_file.open("w", encoding="utf-8") as target:
        for word, count in result:
            target.write(f"{word}\t{count}\n")

    success_file = OUTPUT_DIR / "_SUCCESS"
    success_file.write_text("", encoding="utf-8")

    # Copiar los resultados a la carpeta que revisan las pruebas.
    shutil.copyfile(output_file, SUBMISSION_DIR / "part-00000")
    shutil.copyfile(success_file, SUBMISSION_DIR / "_SUCCESS")


if __name__ == "__main__":
    main()
