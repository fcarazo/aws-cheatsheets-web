#!/usr/bin/env python
import os
from io import BytesIO
from operator import and_, index
from random import randint

import requests
from crewai.flow import Flow, and_, listen, start
from flow_aws_arquitecture.crews.crewai_ai_content_aws.src.crewai_ai_content_aws.crew import (
    AWSCrew,
)
from pdf2image import convert_from_bytes
from pydantic import BaseModel


def download_pdf_and_convert_to_png(pdf_url, output_path="output_image.png"):
    # Descargar el PDF
    response = requests.get(pdf_url)

    if response.status_code == 200:
        print("PDF descargado exitosamente.")

        # Convertir la primera página del PDF a imagen usando convert_from_bytes
        images = convert_from_bytes(response.content)

        # Guardar la primera página como PNG
        image = images[0]  # Primer página
        image.save(output_path, "PNG")
        print(f"Imagen guardada como {output_path}.")
    else:
        print(f"Error al descargar el PDF. Código de estado: {response.status_code}")


class AWSState(BaseModel):
    file_count: int = 1
    html: str = ""


class AWSFlow(Flow[AWSState]):

    @start()
    def generate_urls(self):

        urls = [
            {
                "file_name": "aws-07_AWS-Arquitecture-Identify-Product-Defects-Using-Industrial-Computer-Vision",
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/identify-product-defects-using-industrial-computer-vision-ra.pdf",
            },
        ]
        return urls

    @listen(generate_urls)
    def generate_content(self, urls):
        print("Generating content")
        # Download the PDF and convert it to PNG
        index_ = self.state.file_count - 1
        pdf_url = urls[index_]["url"]
        img_file_name = urls[index_]["file_name"] + ".png"
        img_file_name = os.path.join("../static/img/pubs/principal", img_file_name)
        download_pdf_and_convert_to_png(pdf_url, img_file_name)
        print(f"Image saved as {img_file_name}")
        aws_content_crew = AWSCrew().crew()
        results = aws_content_crew.kickoff_for_each(urls)
        self.state.html = results
        self.state.file_count += 1

        return (results, urls)

    @listen(and_(generate_content, generate_urls))
    def save_content(self, results):
        results, urls = results
        index_ = self.state.file_count - 1
        file_name = urls[index_]["file_name"] + ".html"
        file_name = os.path.join("../templates/pubs/", file_name)
        print(f"Saving content to {file_name}")
        with open(file_name, "w") as f:
            f.write(results)


def kickoff():
    poem_flow = AWSFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = AWSFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
