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

        urls = archivos = [
            {
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/identify-product-defects-using-industrial-computer-vision-ra.pdf",
                "file_name": "aws-07_Arquitectura-Cloud-para-deteccion-de-defectos-en-productos-con-vision-computacional",
            },
            {
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/meter-data-analytics-platform-ra.pdf",
                "file_name": "aws-08_Plataforma-analitica-en-la-nube-para-datos-de-medidores-en-tiempo-real",
            },
            {
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/highbyte-intelligence-hub-industrial-dataops-on-aws-ra.pdf?did=wp_card&trk=wp_card",
                "file_name": "aws-09_Hub-de-inteligencia-industrial-en-AWS-para-optimizar-operaciones",
            },
            {
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/siemens-industrial-edge-on-aws-ra.pdf",
                "file_name": "aws-10_Edge-como-solucion-en-industria-4.0-con-Siemens-y-AWS",
            },
            {
                "url": "https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/siemens-teamcenter-ra.pdf",
                "file_name": "aws-11_Arquitectura-Cloud-para-gestionar-productos-con-Siemens-Teamcenter",
            },
            {
                "url": "https://docs.aws.amazon.com/architecture-diagrams/latest/electric-vehicle-charging-station-management-software/electric-vehicle-charging-station-management-software.html",
                "file_name": "aws-12_Gestion-de-estaciones-de-carga-para-vehiculos-electricos-en-AWS",
            },
        ]

        index_ = self.state.file_count - 1
        file_name = urls[index_]["file_name"] + ".html"
        print(file_name)
        return urls

    @listen(generate_urls)
    def generate_content(self, urls):
        print("Generating content")

        # Iterar sobre cada URL en el listado
        for index_, url_data in enumerate(urls):
            try:
                pdf_url = url_data["url"]
                img_file_name = url_data["file_name"] + ".png"
                img_file_name = os.path.join(
                    "../static/img/pubs/principal", img_file_name
                )

                # Descargar el PDF y convertirlo a PNG
                download_pdf_and_convert_to_png(pdf_url, img_file_name)
                print(f"Image saved as {img_file_name}")
            except:
                print(f"Image not processed: {img_file_name} ")
        # Generar contenido con AWS Crew
        aws_content_crew = AWSCrew().crew()
        results = aws_content_crew.kickoff_for_each(urls)
        self.state.html = results

        return (results, urls)

    @listen(and_(generate_content, generate_urls))
    def save_content(self, results):
        results, urls = results

        # Itera sobre los resultados y las URLs
        for index_, result in enumerate(results):
            file_name = urls[index_]["file_name"] + ".html"
            file_name = os.path.join("../templates/pubs/", file_name)
            print(f"Saving content to {file_name}")

            # Asegúrate de que cada resultado sea una cadena
            if isinstance(result, list):
                result = "".join(result)
            elif not isinstance(result, str):
                result = str(result)

            # Guardar cada archivo HTML
            with open(file_name, "w") as f:
                f.write(result)

        # Incrementar el contador de archivos después de guardar todos
        self.state.file_count += len(results)


def kickoff():
    poem_flow = AWSFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = AWSFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
