import java.util.Random;

public class OpenCRXToken {

    public static void main(String args[]) {
        int length = 40;
        long start = Long.parseLong("1582038122371");
        long stop = Long.parseLong("1582038122769");

        long arg1 = Long.parseLong(args[0]);
        long arg2 = Long.parseLong(args[1]);

        System.out.println("Argument " + arg1);
        System.out.println("Argument " + arg2);
        String token = "";

        for (long l = start; l < stop; l++) {
            token = getRandomBase62(length, l);
            System.out.println(token);
        }
    }

    public static String getRandomBase62(int length, long seed) {
        String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        Random random = new Random(seed);
        StringBuilder s = new StringBuilder();
        for (int i = 0; i < length; i++) {
            s.append(alphabet.charAt(random.nextInt(62)));
        }
        return s.toString();
    }
}
