from docx.oxml.ns import qn, nsdecls
from docx.oxml import OxmlElement
from django.conf import settings
from docxtpl import DocxTemplate
from docx.enum.table import WD_TABLE_ALIGNMENT

import os

import docx
from pathlib import Path
from lxml import etree


class GeneradorAvisoPrivacidad:

    def __init__(self):
        self.respuestas = {}
        self.docto = ""

    # Agrega una nota al pie de página asociada a un texto dentro del párrafo.
    def add_footnote(self, paragraph, footnote_text, run_text=""):
        """
        Agrega una llamada a nota al pie en el párrafo y registra la nota en /word/footnotes.xml
        """
        document = paragraph.part.package.main_document_part

        # 1. Obtener o inicializar la parte footnotes.xml
        try:
            footnotes_part = document.part_related_by(docx.opc.constants.RELATIONSHIP_TYPE.FOOTNOTES)
            # Como footnotes_part es un Part genérico, parseamos su _blob XML
            root_footnotes = etree.fromstring(footnotes_part._blob)
        except KeyError:
            # Si el documento aún no tiene notas al pie, creamos la estructura base obligatoria de Word
            xml_inicial = (
                f'<w:footnotes {nsdecls("w")}>\n'
                f'  <w:footnote w:type="separator" w:id="-1">\n'
                f'    <w:p><w:r><w:separator/></w:r></w:p>\n'
                f'  </w:footnote>\n'
                f'  <w:footnote w:type="continuationSeparator" w:id="0">\n'
                f'    <w:p><w:r><w:continuationSeparator/></w:r></w:p>\n'
                f'  </w:footnote>\n'
                f'</w:footnotes>'
            )
            root_footnotes = etree.fromstring(xml_inicial.encode('utf-8'))
            footnotes_part = docx.opc.part.Part(
                docx.opc.packuri.PackURI('/word/footnotes.xml'),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml',
                xml_inicial.encode('utf-8'),
                document.package
            )
            document.relate_to(footnotes_part, docx.opc.constants.RELATIONSHIP_TYPE.FOOTNOTES)

        # 2. Calcular el siguiente ID numérico disponible
        existing_ids = [
            int(fn.get(qn('w:id')))
            for fn in root_footnotes.findall(qn('w:footnote'))
            if fn.get(qn('w:id')) is not None and int(fn.get(qn('w:id'))) > 0
        ]
        next_id = max(existing_ids, default=0) + 1

        # 3. Construir la entrada XML para la nota al pie
        nueva_nota_xml = (
            f'<w:footnote {nsdecls("w")} w:id="{next_id}">\n'
            f'  <w:p>\n'
            f'    <w:pPr><w:pStyle w:val="Footnot"/></w:pPr>\n'
            f'    <w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>\n'
            f'    <w:r><w:t xml:space="preserve"> {footnote_text}</w:t></w:r>\n'
            f'  </w:p>\n'
            f'</w:footnote>'
        )
        nueva_nota_elem = etree.fromstring(nueva_nota_xml.encode('utf-8'))
        root_footnotes.append(nueva_nota_elem)

        # Guardar el XML actualizado en la parte del paquete
        footnotes_part._blob = etree.tostring(root_footnotes, encoding='utf-8')

        # 4. Insertar la referencia superíndice en el párrafo del documento
        if run_text:
            paragraph.add_run(run_text)

        # Crear el run específico para la referencia
        r = paragraph.add_run()
        rPr = OxmlElement('w:rPr')

        # Aplicar estilo nativo de Word para referencias a nota al pie
        rStyle = OxmlElement('w:rStyle')
        rStyle.set(qn('w:val'), 'Footnot')
        rPr.append(rStyle)

        # Forzar posición de superíndice
        vertAlign = OxmlElement('w:vertAlign')
        vertAlign.set(qn('w:val'), 'superscript')
        rPr.append(vertAlign)

        r._r.append(rPr)

        # Agregar la referencia a la nota
        fn_reference = OxmlElement('w:footnoteReference')
        fn_reference.set(qn('w:id'), str(next_id))
        r._r.append(fn_reference)


    # Agrega un hipervinculo
    def add_hyperlink(self, paragraph, url, text, color="0000FF", underline=True):
        """
        Agrega un hipervínculo (URL o email) a un párrafo de python-docx.
        """
        # 1. Obtener la relación para el documento
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

        # 2. Crear los elementos XML para el hyperlink
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), r_id)

        # 3. Crear el Run interno con el texto visible
        new_run = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')

        # Color del texto (por defecto azul)
        if color:
            c = OxmlElement('w:color')
            c.set(qn('w:val'), color)
            rPr.append(c)

        # Subrayado
        if underline:
            u = OxmlElement('w:u')
            u.set(qn('w:val'), 'single')
            rPr.append(u)

        new_run.append(rPr)

        # Añadir el texto del enlace
        text_node = OxmlElement('w:t')
        text_node.text = text
        new_run.append(text_node)

        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

        return hyperlink

    # Define el nombre del archivo
    def obtener_nombre_unico(self, ruta_base):
        if not os.path.exists(ruta_base):
            return ruta_base

        # Separa el directorio y nombre de la extensión (ej. "nombre" y ".docx")
        directorio, nombre_completo = os.path.split(ruta_base)
        nombre, extension = os.path.splitext(nombre_completo)

        contador = 1
        nueva_ruta = os.path.join(directorio, f"{nombre} ({contador}){extension}")

        # Incrementa el contador mientras el archivo siga existiendo
        while os.path.exists(nueva_ruta):
            contador += 1
            nueva_ruta = os.path.join(directorio, f"{nombre} ({contador}){extension}")

        return nueva_ruta
    #### Tabla
    def borde_inferior(self, celda, color="808080", grosor="8"):
        tcPr = celda._tc.get_or_add_tcPr()

        tcBorders = tcPr.find(qn("w:tcBorders"))

        if tcBorders is None:
            tcBorders = OxmlElement("w:tcBorders")
            tcPr.append(tcBorders)

        bottom = tcBorders.find(qn("w:bottom"))

        if bottom is None:
            bottom = OxmlElement("w:bottom")
            tcBorders.append(bottom)

        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), grosor)
        bottom.set(qn("w:color"), color)

    ##### SECCIONES
    def escribir_titulo(self, tipo):
        doc = docx.Document(self.docto)

        doc.add_paragraph("AVISO DE PRIVACIDAD "+ tipo, style='superTit')
        doc.add_paragraph(self.respuestas['nombreTratamiento'], style='superTit')

        doc.add_paragraph("", style='Parraf')

        doc.save(self.docto)

    def escribir_seccion1(self, sec1):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("I. Denominación y domicilio del responsable")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisitos previstos por los artículos 20 y 21, fracción I de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿Quién es el responsable del tratamiento de los datos personales?")

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("La " + self.respuestas['sujetoObligado'] + ", a través de la " + self.respuestas['unidadAdmin'] + ", con domicilio en " + sec1.direccion_texto() + ", es el área administrativa responsable del tratamiento de los datos personales que nos proporcione, los cuales serán protegidos conforme a lo dispuesto por la Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados (Ley General de Datos), la Ley General de Transparencia y Acceso a la Información Pública (Ley General de Transparencia), y demás disposiciones jurídicas aplicables.", style='Parraf')
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Los datos personales recabados, serán incorporados y tratados en el sistema denominado:", style='Parraf')
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph(self.respuestas['nombreTratamiento'], style='Parraf')
        doc.add_paragraph("", style='Parraf')
        doc.save(self.docto)

    def escribir_seccion2(self, sec2):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run(
            "II. Datos personales sometidos a tratamiento, identificando los que son sensibles")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción II de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" / ¿Qué datos personales se recaban?")

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("De conformidad con el artículo 3, fracciones IX y X, de la Ley General de Protección de Datos Personales en Posesión de los Sujetos Obligados (Ley General de Datos), se entienden por datos personales y datos personales sensibles, los siguientes:",
                          style='Parraf')
        doc.add_paragraph("", style='Parraf')

        pDatos1 = doc.add_paragraph(style='Vineta')
        pDatos1.add_run("Datos personales: ").bold = True
        pDatos1.add_run("Cualquier información concerniente a una persona identificada o identificable. Se considera que una persona es identificable cuando su identidad pueda determinarse directa o indirectamente a través de cualquier información.")
        doc.add_paragraph("", style='Parraf')

        pDatos2 = doc.add_paragraph(style='Vineta')
        pDatos2.add_run("Datos personales sensibles: ").bold = True
        pDatos2.add_run("Aquellos que se refieran a la esfera más íntima de la persona titular, o cuya utilización indebida pueda dar origen a discriminación o conlleve un riesgo grave para ésta. De manera enunciativa más no limitativa, se consideran sensibles los datos personales que puedan revelar aspectos como origen racial o étnico, estado de salud presente o futuro, información genética, creencias religiosas, filosóficas y morales, opiniones políticas y preferencia sexual.")
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Asimismo, por tratamiento debe entenderse cualquier operación o conjunto de operaciones efectuadas mediante procedimientos manuales o automatizados aplicados a los datos personales, relacionadas con la obtención, uso, registro, organización, conservación, elaboración, utilización, comunicación, difusión, almacenamiento, posesión, acceso, manejo, aprovechamiento, divulgación, transferencia o disposición de datos personales, tal como lo previene el artículo 3, fracción XXXI, de la Ley General de Datos.",
                          style='Parraf')
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Una vez señalado lo anterior, se hace de su conocimiento que la " + self.respuestas['unidadAdmin'] + ", recaba, procesa y utiliza diversos datos personales de identificación y contacto de las personas titulares, los cuáles se señalan a continuación:",
                          style='Parraf')
        doc.add_paragraph("", style='Parraf')

        # # DATOS PERSONALES
        # for data in sec2:
        #     doc.add_paragraph(data.dato, style='Vineta')
        #     doc.add_paragraph("", style='Parraf')
        #     print(data.dato)
        #
        # doc.add_paragraph("Los medios a través de los cuales se obtienen los datos personales son:",
        #                   style='Parraf')
        # doc.add_paragraph("", style='Parraf')
        #
        # # MEDIOS PARA RECABAR
        # for data in sec2:
        #     doc.add_paragraph(data.get_medioObtencion_display(), style='Vineta')
        #     doc.add_paragraph("", style='Parraf')
        #     print(data.dato)

        # ----------------- tabla
        tabla =doc.add_table(rows=1, cols=3)

        encabezados = ["Dato personal", "Tipo de dato", "Medio de obtención"]

        for celda, texto in zip(tabla.rows[0].cells, encabezados):
            celda.text = texto
            # self.color_celda(celda, "E5E5E5")
            self.borde_inferior(celda, color="808080", grosor="8")

            for parrafo in celda.paragraphs:
                parrafo.style = "EncabezadoTabla"

        for i, data in enumerate(sec2):
            celdas = tabla.add_row().cells

            celdas[0].text = data.dato
            celdas[1].text = "Sensibles" if data.datosSensibles else "No sensible"
            celdas[2].text = data.get_medioObtencion_display()

            # Alternar colores
            if i % 2 == 1:
                for celda in celdas:
                    self.color_celda(celda, "E5E5E5")

            # Aplicar estilo a todas las celdas
            for celda in celdas:
                for parrafo in celda.paragraphs:
                    parrafo.style = "Parraf"
        # ----------------- tabla

        doc.add_paragraph("", style='Parraf')

        # doc.add_paragraph("En virtud de lo anterior, se informa que la " + self.respuestas['unidadAdmin'] + " recaba datos personales sensibles, no obstante, eventualmente podrá establecer medidas de seguridad adecuadas cuando se encuentre en presencia de datos personales sensibles, así como de la información a la cual tenga acceso con motivo de sus funciones de carácter clasificado.",
        #                   style='Parraf')
        # doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Por otra parte, también resulta importante mencionar que de conformidad con el artículo 4, párrafo segundo de la Ley General de Transparencia, toda la información generada, obtenida, adquirida, transformada o en posesión de los sujetos obligados es pública y accesible a cualquier persona, en los términos y condiciones que se establezcan en la Ley General de Transparencia, en los tratados internacionales de los que el Estado mexicano sea parte, las leyes de las entidades federativas y en las disposiciones jurídicas aplicables dentro de sus respectivas competencias, así como de conformidad con el párrafo tercero del artículo 4 de la Ley General de Transparencia la información podrá ser clasificada como reservada temporalmente por razones de interés público o seguridad nacional conforme a los términos establecidos por la Ley General de Transparencia.",
                          style='Parraf')
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("En consecuencia, la información contenida en los archivos de la " + self.respuestas['unidadAdmin'] + " es susceptible de considerarse información pública, inclusive los datos personales que, por disposición de la Ley General de Transparencia, sean considerados como información pública (por ejemplo, datos de identificación de servidoras y servidores públicos).",
                          style='Parraf')
        doc.add_paragraph("", style='Parraf')

        doc.save(self.docto)

    def escribir_seccion3(self, sec3):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("III. Fundamento legal que faculta a la " + self.respuestas['unidadAdmin'] + " para llevar a cabo el tratamiento de datos personales")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción III de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" / ¿Cuál es el fundamento legal para el tratamiento?")

        doc.add_paragraph("", style='Parraf')

        if not sec3:
            doc.add_paragraph("No se especificaron fundamentos legales.", style='Vineta')
            return

        print(sec3)
        for fundamento in sec3:
            doc.add_paragraph(fundamento.especificacion+" de la "+fundamento.ley, style='Vineta')
            print(fundamento.ley)

        doc.add_paragraph("", style='Parraf')

        doc.save(self.docto)

    def escribir_seccion4(self, sec4, numero = "IV"):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run(numero +". Finalidades del tratamiento para las cuales se obtienen los datos personales distinguiendo aquellas que requieren el consentimiento de la persona titular")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción IV de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿Cuáles son las finalidades del tratamiento?")

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Los datos personales recabados, serán utilizados para las siguientes finalidades:", style='Parraf')

        doc.add_paragraph("", style='Parraf')

        if not sec4:
            doc.add_paragraph("No se especificaron finalidades.", style='Vineta')
            return
        else:
            if numero == "II":
                for fin in sec4:
                    doc.add_paragraph(fin.finalidad, style='Vineta')
                    doc.add_paragraph("", style='Parraf')
                    print(fin.finalidad)
            else:
                # ----------------- tabla
                tabla = doc.add_table(rows=1, cols=2)

                encabezados = ["Finalidad", "Detalles"]

                for celda, texto in zip(tabla.rows[0].cells, encabezados):
                    celda.text = texto
                    self.borde_inferior(celda, color="808080", grosor="8")

                    for parrafo in celda.paragraphs:
                        parrafo.style = "EncabezadoTabla"

                for i,data in enumerate(sec4):
                    celdas = tabla.add_row().cells

                    celdas[0].text = data.finalidad
                    if data.necesaria:
                        celdas[1].text = "Necesaria"
                    else:
                        if data.reqConsentimiento:
                            celdas[1].text = "Opcional, requiere consentimiento " + data.get_tipoConsentimiento_display()
                            if data.get_tipoConsentimiento_display() == "Expreso":
                                celdas[1].text += "___________"
                        else:
                            celdas[1].text = "Opcional"

                    # Alternar colores
                    if i % 2 == 1:
                        for celda in celdas:
                            self.color_celda(celda, "E5E5E5")

                    # Aplicar estilo a todas las celdas
                    for celda in celdas:
                        for parrafo in celda.paragraphs:
                            parrafo.style = "Parraf"

                # ----------------- tabla

        doc.add_paragraph("", style='Parraf')

        # doc.add_paragraph(
        #     "Por regla general, el consentimiento para el tratamiento de sus datos personales será tácito, es decir, cuando habiéndose puesto a disposición de la persona titular el presente aviso de privacidad, ésta o éste no manifieste su voluntad en sentido contrario; por lo tanto, no se requerirá autorización expresa para el tratamiento de datos personales, en el entendido que usted autoriza de manera tácita a la " + self.respuestas['acronUnidadAdmin'] + " para el tratamiento de sus datos personales en términos del presente aviso de privacidad.",
        #     style='Parraf')
        #
        # doc.add_paragraph("", style='Parraf')

        doc.save(self.docto)

    def escribir_seccion5_6(self, sec5, sec6):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("\nV y VI. Domicilio de la Unidad de Transparencia y mecanismos, medios y procedimientos disponibles para ejercer los derechos de Acceso, Rectificación, Cancelación u Oposición.")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracciones V y VI de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿Dónde está ubicada la Unidad y Transparencia? ¿Ante quién se realiza el ejercicio de los Derechos ARCO?")

        doc.add_paragraph("", style='Parraf')


        p = doc.add_paragraph(style='Parraf')
        p.add_run("Usted podrá ejercer sus derechos de acceso, rectificación, cancelación u oposición de sus datos personales directamente ante la Unidad de Transparencia de la ")
        p.add_run(self.respuestas['sujetoObligado']+", ubicada en "+sec6.direccion_texto()+"; número telefónico y extensión: ")
        p.add_run("; número telefónico y extensión: "+sec6.telefono_texto()+", extensiones "+sec6.extension)
        p.add_run(", correo electrónico "+sec6.correo+".")
        # self.add_hyperlink(p, "https://www.plataformadetransparencia.org.mx/web/guest/inicio","https://www.plataformadetransparencia.org.mx/web/guest/inicio")
        # p.add_run(", en el apartado de Solicitudes de Datos Personales.")

        doc.add_paragraph(
            sec5.procARCO,
            style='Parraf')

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph(
            "Asimismo, si desea recibir asesoría para el ejercicio de estos derechos puede acudir directamente a la Unidad de Transparencia, enviar un correo electrónico a la dirección antes señalada o comunicarse al número y extensión indicada.",
            style='Parraf')

        doc.add_paragraph("", style='Parraf')

        print(sec5)
        print(sec6)

        doc.save(self.docto)

    # Función para colorear celdas
    def color_celda(self, celda, color):
        tcPr = celda._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), color)
        tcPr.append(shd)

    def escribir_seccion7(self, sec7, numero = "VII"):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("\n"+numero+". Transferencias de datos personales")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción VII de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿A quién se transfieren los datos personales?")




        if sec7 and sec7.exists():
            # ----------------- tabla
            tabla = doc.add_table(rows=1, cols=3)
            tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
            tabla.autofit = False

            encabezados = ["Destinatario", "Finalidad", "Consentimiento"]

            for celda, texto in zip(tabla.rows[0].cells, encabezados):
                celda.text = texto
                self.borde_inferior(celda, color="808080", grosor="8")

                for parrafo in celda.paragraphs:
                    parrafo.style = "EncabezadoTabla"

            for i,data in enumerate(sec7):
                celdas = tabla.add_row().cells

                celdas[0].text = data.destinatario
                celdas[1].text = data.finalidades_formateadas()
                celdas[2].text = "¿Da su consentimiento? ________" if data.consentimiento else "No requiere consentimiento"

                # Alternar colores
                if i % 2 == 1:
                    for celda in celdas:
                        self.color_celda(celda, "E5E5E5")

                # Aplicar estilo a todas las celdas
                for celda in celdas:
                    for parrafo in celda.paragraphs:
                        parrafo.style = "Parraf"
            # ----------------- tabla
        else:
            p = doc.add_paragraph(style='Parraf')
            p.add_run("Se hace de su conocimiento que sólo se realizarán transferencias de datos personales, cuando éstas sean necesarias para atender requerimientos de información de una autoridad competente, por lo que, de conformidad con lo dispuesto por los artículos 16, fracción III y 64, fracciones III, IV, VIII y IX de la Ley General de Datos, no se requiere de su consentimiento para la transferencia de sus datos personales en atención a un requerimiento de autoridad competente, como pudiera ser el caso del Poder Judicial de la Federación en razón a los juicios de amparo que como persona titular puede interponer para la salvaguarda de sus derechos, de conformidad con el artículo 1, fracción I de la Ley de Amparo, Reglamentaria de los artículos 103 y 107 de la Constitución Política de los Estados Unidos Mexicanos. ")
            self.add_hyperlink(p, "https://www.plataformadetransparencia.org.mx/web/guest/inicio", "https://www.plataformadetransparencia.org.mx/web/guest/inicio")
            p.add_run(", en el apartado de Solicitudes de Datos Personales.")

        # doc.add_paragraph(
        #     "Asimismo, si desea conocer el procedimiento y/o recibir asesoría para el ejercicio de estos derechos puede acudir directamente a la Unidad de Transparencia, enviar un correo electrónico a la dirección antes señalada o comunicarse al número y extensión indicada.",
        #     style='Parraf')

        doc.add_paragraph("", style='Parraf')

        # print(sec7)

        doc.save(self.docto)

    def escribir_seccion8(self, sec8, numero = "VIII"):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run(
            numero+". Mecanismos y medios disponibles para que la persona titular pueda manifestar su negativa para el tratamiento de sus datos personales")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción VIII de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿Cómo se puede manifestar la negativa para el tratamiento o transferencia de datos personales?")

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph(sec8.manifestacion, style='Parraf')
        doc.add_paragraph("", style='Parraf')

        # doc.add_paragraph('No obstante, para cualquier asunto relacionado también podrá establecer comunicación directa al correo electrónico ...', style='Parraf')
        #
        # doc.add_paragraph("", style='Parraf')
        doc.save(self.docto)

    def escribir_seccion9(self, sec9):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("IX. Medios para comunicar a las personas titulares de los datos personales los cambios realizados al aviso de privacidad.")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción IX y 22, primer párrafo de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿Dónde se pueden conocer los cambios efectuados a este aviso de privacidad?")

        doc.add_paragraph("", style='Parraf')

        # doc.add_paragraph("Se entiende que el aviso de privacidad integral es puesto a disposición de las personas titulares de manera permanente, en las instalaciones de la " + self.respuestas['acronSujetoObligado'] + ", cuya ubicación ha quedado señalada en el primer apartado de este documento. La " + self.respuestas['acronSujetoObligado'] + ", la " + self.respuestas['unidadAdmin'] + " podrán establecer medidas de seguridad especiales para la recepción y envío de datos personales en función de las características observadas con el manejo de datos personales o información clasificada y/o susceptible de incurrir en supuestos de clasificación." + self.respuestas['fechahoy'], style='Parraf')
        # doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Los cambios y/o modificaciones a los avisos de privacidad integral y simplificado se identificarán en cada documento conforme a la última actualización que corresponda, en caso de requerir acceso a versiones previas, se sugiere establecer contacto con la " + self.respuestas['unidadAdmin'] + " a través de los datos que se indican al final del presente documento. No obstante, la versión actualizada y vigente del presente aviso de privacidad, a través de: ", style='Parraf')
        # self.add_hyperlink(p, sec9.url, sec9.url)

        PUBLICA_MODIFICACIONES = {
            'W': 'Portal Institucional.',
            'E': 'Estrados.',
            'M': 'Micrositio.',
            'O': 'Otro.',
        }

        for modificacion in sec9.modificaciones:
            texto = PUBLICA_MODIFICACIONES.get(modificacion)
            if texto:
                doc.add_paragraph(texto, style='Vineta')

        p = doc.add_paragraph("URL disponible: ", style='Vineta')
        self.add_hyperlink(p, sec9.url, sec9.url)

        doc.add_paragraph("", style='Parraf')
        doc.save(self.docto)


    def escribir_conocerAvP(self, sec9):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("V. Lugar para conocer el Aviso de Privacidad Integral.")
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="Requisito previsto por el artículo 21, fracción IX y 22, primer párrafo de la Ley General de Datos.",
            run_text=""
        )
        p_titulo.add_run(" /¿En dónde se puede conocer el aviso de privacidad integral?")

        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("Se entiende que el aviso de privacidad integral es puesto a disposición de las personas titulares de manera permanente, en las instalaciones de la " + self.respuestas['acronSujetoObligado'] + ", cuya ubicación ha quedado señalada en el primer apartado de este documento.", style='Parraf')
        doc.add_paragraph("", style='Parraf')

        p = doc.add_paragraph(style='Parraf')
        p.add_run("La versión actualizada y vigente del aviso de privacidad integral, se podrá conocer a través de: ")
        self.add_hyperlink(p, sec9.url, sec9.url)
        p.add_run(".")

        doc.add_paragraph("", style='Parraf')
        doc.save(self.docto)

    def escribir_portabilidad(self, secPortabilidad):
        doc = docx.Document(self.docto)

        p_titulo = doc.add_paragraph(style='Titu')
        p_titulo.add_run("Portabilidad, exclusiones e información de contacto con " + self.respuestas['unidadAdmin'] )
        self.add_footnote(
            paragraph=p_titulo,
            footnote_text="En reconocimiento al derecho establecido en el artículo 51 de la Ley General de Datos, para la obtención de una copia de los datos en formato electrónico estructurado y comúnmente utilizado.",
            run_text=""
        )
        p_titulo.add_run(" /¿Cómo se puede ejercer el derecho a la portabilidad de datos personales?")

        doc.add_paragraph("", style='Parraf')

        if secPortabilidad.portabilidad and secPortabilidad.portabilidad.strip():
            # Tiene contenido válido
            doc.add_paragraph(secPortabilidad.portabilidad, style='Parraf')
        else:
            # Texto para una negativa
            doc.add_paragraph("Este tratamiento de datos personales no se encuentra en formatos estructurados y comúnmente utilizados para su portabilidad, en términos de lo dispuesto en los artículos 51 de la Ley General de Datos que establece los parámetros, y procedimientos para la portabilidad de datos personales.", style='Parraf')

        doc.add_paragraph("", style='Parraf')
        doc.save(self.docto)

    def escribir_infoAdicional(self, observaciones):
        doc = docx.Document(self.docto)

        doc.add_paragraph("Información adicional", style='Titu')
        doc.add_paragraph("", style='Parraf')

        doc.add_paragraph("A fin de obtener mayor información respecto al tratamiento de datos personales a cargo de la " + self.respuestas['unidadAdmin'] + ", se le sugiere establecer comunicación a través del correo electrónico: " + self.respuestas['unidadAdmin'] + ", o presencialmente, en el domicilio ubicado en " + self.respuestas['direccion'] + ", en un horario de lunes a viernes de 9:00 a 18:00 horas.", style='Parraf')
        doc.add_paragraph("", style='Parraf')

        if observaciones:
            # doc.add_paragraph(observaciones, style='Parraf')
            print(repr(observaciones))
            observaciones = observaciones.strip()
            partes = observaciones.splitlines()

            parrafo = doc.add_paragraph(style="Parraf")

            for i, parte in enumerate(partes):
                if i > 0:
                    parrafo.add_run().add_break()

                parrafo.add_run(parte)

            doc.add_paragraph("", style='Parraf')

        doc.save(self.docto)

    def escribir_fecha(self):
        doc = docx.Document(self.docto)

        p = doc.add_paragraph(style='Fech')
        p.add_run("Fecha de elaboración: ").bold = True
        p.add_run(self.respuestas['fechahoy'])
        doc.save(self.docto)

    # Almacenar datos en self - datos que se reutilicen en el documento
    def completar_datos(self, cuestionario, fecha, sec1, sec2):
        self.respuestas['sujetoObligado'] = cuestionario.sujetoObligado

        self.respuestas['fechahoy'] = fecha

        self.respuestas['unidadAdmin'] = sec1.unidadAdmin
        self.respuestas['acronSujetoObligado'] = sec1.acronSujetoObligado
        self.respuestas['acronUnidadAdmin'] = sec1.acronUnidadAdmin
        self.respuestas['direccion'] = sec1.direccion_texto()

        self.respuestas['nombreTratamiento'] = sec2.nombreTratamiento

    # Crear documento
    def crearDocto(self, nombrearchivo):
        ruta_plantilla = (settings.PLANTILLAS_DOCX/ "plantillaAvp.docx")
        doc = DocxTemplate(ruta_plantilla)

        self.docto = Path(settings.BASE_DIR) / nombrearchivo

        doc.save(self.docto)

        print("¡Documento generado exitosamente!")
