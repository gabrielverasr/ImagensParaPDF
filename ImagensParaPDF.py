import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PyQt5.QtGui import QFont


class ImageToPdfWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pdf_counter = 1  # Iniciar o contador de PDFs

    def initUI(self):
        self.setWindowTitle("Converter Imagens para PDF - por Gabriel ℣eras")
        self.setFixedSize(650, 250)

        layout = QVBoxLayout()

        # Incluir símbolo ℣
        symbol_label = QLabel("🖼 ℣")
        symbol_label.setAlignment(Qt.AlignCenter)  # Alinhar o texto ao centro
        font = QFont("DejaVu Sans", 30)  # Especificar a fonte "DejaVu Sans" e o tamanho da fonte desejado
        symbol_label.setFont(font)
        layout.addWidget(symbol_label)

        
        
        # Incluir instruções
        instructions_label = QLabel("Selecione as imagens e clique no botão para converter em PDF:")
        instructions_label.setWordWrap(True)  # Ativar quebra de linha automática
        instructions_label.setAlignment(Qt.AlignCenter)  # Alinhar o texto ao centro
        font = instructions_label.font()
        font.setPointSize(12)  
        # Ajuste o tamanho da fonte para o valor desejado
        instructions_label.setFont(font)
        layout.addWidget(instructions_label)



        button = QPushButton("👉 Clique aqui para selecionar as imagens")
        font = button.font()
        font.setPointSize(12)  
        # Ajuste o tamanho da fonte para o valor desejado
        button.setFont(font)
        button.clicked.connect(self.select_images)
        layout.addWidget(button)


        # Incluir instruções 2
        instructions_label = QLabel("📄 O arquivo será gerado na sua Área de Trabalho.")
        instructions_label.setWordWrap(True)  # Ativar quebra de linha automática
        instructions_label.setAlignment(Qt.AlignCenter)  # Alinhar o texto ao centro
        font = instructions_label.font()
        font.setPointSize(8)  
        # Ajuste o tamanho da fonte para o valor desejado
        instructions_label.setFont(font)
        layout.addWidget(instructions_label)
        
        # Créditos
        instructions_label = QLabel("Créditos: Gabriel Veras <a href='http://www.gabrielveras.art'>www.gabrielveras.art</a>")
        instructions_label.setWordWrap(True)
        instructions_label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 8)
        instructions_label.setFont(font)
        instructions_label.setOpenExternalLinks(True)  # Permitir que o link seja aberto no navegador padrão
        layout.addWidget(instructions_label)

        self.setLayout(layout)
        self.show()

        self.setLayout(layout)
        self.show()

    def select_images(self):
        try:
            image_paths, _ = QFileDialog.getOpenFileNames(self, "Selecione as imagens", "", "Imagens (*.jpeg *.jpg *.png)")

            if image_paths:
                self.create_pdf(image_paths)

        except Exception as e:
            error_message = f"Ocorreu um erro ao selecionar as imagens:\n{str(e)}"
            QMessageBox.critical(self, "Erro", error_message)

    def create_pdf(self, image_paths):
        # Definir o nome do arquivo PDF com base no contador
        pdf_filename = self.get_unique_pdf_filename()

        # Incrementar o contador de PDFs para o próximo PDF
        self.pdf_counter += 1

        # Criar o arquivo PDF
        pdf = canvas.Canvas(pdf_filename, pagesize=letter)

        for image_path in image_paths:
            png_path = os.path.splitext(image_path)[0] + ".png"
            self.convert_to_png(image_path, png_path)

            img = ImageReader(png_path)
            img_width, img_height = img.getSize()

            # Ajustar o tamanho da página do PDF de acordo com a imagem
            pdf.setPageSize((img_width, img_height))
            pdf.drawImage(img, 0, 0, width=img_width, height=img_height)
            pdf.showPage()

        # Salvar o PDF final
        pdf.save()

        QMessageBox.information(self, "Sucesso", f"PDF criado com sucesso na sua área de trabalho!")

    def convert_to_png(self, input_path, output_path):
        from PIL import Image

        image = Image.open(input_path)
        image.save(output_path, "PNG")

    def get_unique_pdf_filename(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        pdf_filename = os.path.join(desktop_path, f"ImagensParaPDF_{self.pdf_counter}.pdf")
        while os.path.exists(pdf_filename):
            self.pdf_counter += 1
            pdf_filename = os.path.join(desktop_path, f"ImagensParaPDF_{self.pdf_counter}.pdf")
        return pdf_filename

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageToPdfWindow()
    sys.exit(app.exec_())