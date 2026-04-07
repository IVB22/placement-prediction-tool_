package com.futurepath.util;

import java.io.File;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

public final class PdfUtil {
  private PdfUtil() {}

  public static String extractText(String path) {
    try (PDDocument doc = Loader.loadPDF(new File(path))) {
      return new PDFTextStripper().getText(doc);
    } catch (Exception e) {
      return "";
    }
  }
}
