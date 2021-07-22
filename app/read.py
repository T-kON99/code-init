import sys
import locale
import os
import ghostscript


def pdfToText(pdfFile, outputFile):
    args = [
        "pdf2text",  # actual value doesn't matter
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=txtwrite",
        "-sOutputFile=" + outputFile,
        "-f",
        pdfFile,
    ]
    # arguments have to be bytes, encode them
    encoding = locale.getpreferredencoding()
    args = [_.encode(encoding) for _ in args]

    ghostscript.Ghostscript(*args)


def iteratePDFsFrom(path: str):
    for root, directory, files in os.walk(path):
        for file in files:
            if ".pdf" in file:
                yield os.path.join(root, file)


def processText(savePath: str, encoding="CP1252"):
    with open(savePath, mode="r", encoding=encoding) as file:
        data = [
            ",".join(list(filter(lambda x: x != "" and x != "=", _.strip().split(" "))))
            for _ in file.readlines()
        ]
    print(data)
    with open(savePath, mode="w+") as file:
        for _ in data:
            file.write(f"{_}\n")


def pdfToCSV(input_directory: str, output_directory: str):
    count = 0
    count_skip = 0
    for pdfPath in iteratePDFsFrom(input_directory):
        outputPath = output_directory
        try:
            os.makedirs(outputPath)
        except FileExistsError:
            pass
        pdfFileName, _ = os.path.splitext(os.path.basename(pdfPath))
        print(f"Processing {pdfFileName}.pdf")
        savePath = f"{outputPath}{pdfFileName}.csv"
        if not os.path.isfile(savePath):
            pdfToText(pdfPath, savePath)
            processText(savePath)
            count += 1
        else:
            count_skip += 1
    return count, count_skip


if __name__ == "__main__":
    INPUT_DIRECTORY = "\\pdf 2\\"
    OUTPUT_DIRECTORY = "/processed 2/"
    pdfToCSV(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
