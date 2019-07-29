import com.google.zxing.*;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.oned.EAN13Reader;
import org.imgscalr.Scalr;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Zxing1 {

  public static void main(String[] args) {
    File folder = new File("FirstBarcode/src/resource/EAN13");
    File[] listOfFiles = folder.listFiles();
    int recognizables = 0;
    long start = System.currentTimeMillis();

    for (int i = 0; i < listOfFiles.length; i++) {
      File file = listOfFiles[i];
      System.out.print(file.getName() + ": ");
      BufferedImage image = null;
      BinaryBitmap bitmap = null;
      Result result = null;
      try {
        image = ImageIO.read(file);
//                System.out.println("Before resize: width-" + image.getWidth() + "|height-" + image.getHeight());
//            Dimension newMaxSize = new Dimension(220, 160);
//            image = Scalr.resize(image, Scalr.Method.QUALITY, newMaxSize.getWidth(), newMaxSize.getHeight());
//                System.out.println("After resize: width-" + image.getWidth() + "|height-" + image.getHeight());

        int[] pixels = image
            .getRGB(0, 0, image.getWidth(), image.getHeight(), null, 0, image.getWidth());
        RGBLuminanceSource source = new RGBLuminanceSource(image.getWidth(), image.getHeight(),
            pixels);
        bitmap = new BinaryBitmap(new HybridBinarizer(source));
      } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
      }

      EAN13Reader reader = new EAN13Reader();
      try {
        result = reader.decode(bitmap);
        System.out.println(result.getText());
        recognizables++;

      } catch (NotFoundException e) {
        System.out.println(e.getMessage());
      } catch (FormatException e) {
        System.out.println(e.getMessage());
      }
    }
    long finish = System.currentTimeMillis();
    System.out.println((float)recognizables/listOfFiles.length);
    System.out.println((float)(finish-start)/listOfFiles.length);

  }

}
