import com.google.zxing.*;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.oned.EAN13Reader;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.imgscalr.Scalr.*;

/*
 Classify images are EAN13 decodable or not, output to 2 folders (decodable or not)
 */

public class EAN13Classifier {

    public static void main(String[] args) throws IOException {
        String inputPath = args[0];
        String recognizablePath = args[1];
        File recFolder = new File(recognizablePath);
        recFolder.mkdirs();
        String unrecognizablePath = args[2];
        File unrecFolder = new File(unrecognizablePath);
        unrecFolder.mkdirs();

        File folder = new File(inputPath);
        File[] listOfFiles = folder.listFiles();
        Util aPane = new Util();
        //TODO : change to Barcode type we want
        EAN13Reader reader = new EAN13Reader();

        for (int i = 0; i < listOfFiles.length; i++) {
            File file = listOfFiles[i];
            BufferedImage image, image90, imageFV, imageFH, imageB, imageD, image15, image30, image45, image60, image75,
                    imageN15, imageN30, imageN45, imageN60, imageN75;
            try {
                image = ImageIO.read(file);
                image90 = rotate(image, Rotation.CW_90);
                imageFV = rotate(image, Rotation.FLIP_VERT);
                imageFH = rotate(image, Rotation.FLIP_HORZ);
                imageB = apply(image, OP_BRIGHTER);
                imageD = apply(image, OP_DARKER);
                image15 = aPane.rotateImageByDegrees(image, 15);
                image30 = aPane.rotateImageByDegrees(image, 30);
                image45 = aPane.rotateImageByDegrees(image, 45);
                image60 = aPane.rotateImageByDegrees(image, 60);
                image75 = aPane.rotateImageByDegrees(image, 75);
                imageN15 = aPane.rotateImageByDegrees(image, -15);
                imageN30 = aPane.rotateImageByDegrees(image, -30);
                imageN45 = aPane.rotateImageByDegrees(image, -45);
                imageN60 = aPane.rotateImageByDegrees(image, -60);
                imageN75 = aPane.rotateImageByDegrees(image, -75);

                if (isDecodable(image, reader)
                        || isDecodable(image90, reader) || isDecodable(imageFV, reader) || isDecodable(imageFH, reader)
                        || isDecodable(imageB, reader) || isDecodable(imageD, reader)
                        || isDecodable(image15, reader) || isDecodable(image30, reader) || isDecodable(image45, reader)
                        || isDecodable(image60, reader) || isDecodable(image75, reader)
                        || isDecodable(imageN15, reader) || isDecodable(imageN30, reader) || isDecodable(imageN45, reader)
                        || isDecodable(imageN60, reader) || isDecodable(imageN75, reader)
                )
                    Files.copy(file.toPath(), Paths.get(recognizablePath, file.getName()));
                else Files.copy(file.toPath(), Paths.get(unrecognizablePath, file.getName()));
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    static boolean isDecodable(BufferedImage img, Reader reader) {
        int[] pixels = img
                .getRGB(0, 0, img.getWidth(), img.getHeight(), null, 0, img.getWidth());
        RGBLuminanceSource source = new RGBLuminanceSource(img.getWidth(), img.getHeight(),
                pixels);
        BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));
        try {
            reader.decode(bitmap);
            return true;
        } catch (NotFoundException | FormatException | ChecksumException e) {
            return false;
        }
    }

    public static class Util extends JPanel {
        BufferedImage rotateImageByDegrees(BufferedImage img, double angle) {
            double rads = Math.toRadians(angle);
            double sin = Math.abs(Math.sin(rads)), cos = Math.abs(Math.cos(rads));
            int w = img.getWidth();
            int h = img.getHeight();
            int newWidth = (int) Math.floor(w * cos + h * sin);
            int newHeight = (int) Math.floor(h * cos + w * sin);

            BufferedImage rotated = new BufferedImage(newWidth, newHeight, BufferedImage.TYPE_INT_ARGB);
            Graphics2D g2d = rotated.createGraphics();
            AffineTransform at = new AffineTransform();
            at.translate((newWidth - w) / 2, (newHeight - h) / 2);

            int x = w / 2;
            int y = h / 2;

            at.rotate(rads, x, y);
            g2d.setTransform(at);
            g2d.drawImage(img, 0, 0, this);
            g2d.drawRect(0, 0, newWidth - 1, newHeight - 1);
            g2d.dispose();

            return rotated;
        }
    }

}
