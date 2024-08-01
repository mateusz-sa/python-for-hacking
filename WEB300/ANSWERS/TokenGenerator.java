import java.util.Random;
import java.util.Base64;

public class TokenGenerator {

    private static final String CHAR_LOWER = "abcdefghijklmnopqrstuvwxyz";
    private static final String CHAR_UPPER = CHAR_LOWER.toUpperCase();
    private static final String NUMBERS = "1234567890";
    private static final String SYMBOLS = "!@#$%^&*()";
    public static final String CHARSET = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".toUpperCase() + "1234567890" + "!@#$%^&*()";
    private static final int TOKEN_LENGTH = 42;

    public static void main(String[] args) {
        if (args.length != 3) {
            System.out.println("Usage: java TokenGenerator <userId> <startTimestamp> <endTimestamp>");
            return;
        }

        int userId = Integer.parseInt(args[0]);
        long startTimestamp = Long.parseLong(args[1]);
        long endTimestamp = Long.parseLong(args[2]);

        for (long timestamp = startTimestamp; timestamp <= endTimestamp; timestamp++) {
            String token = createToken(userId, timestamp);
            System.out.println(token);
        }
    }

    public static String createToken(int userId, long seed) {
        Random random = new Random(seed);
        StringBuilder sb = new StringBuilder();
        byte[] encbytes = new byte[TOKEN_LENGTH];

        for (int i = 0; i < TOKEN_LENGTH; i++) {
            sb.append(CHARSET.charAt(random.nextInt(CHARSET.length())));
        }

        byte[] bytes = sb.toString().getBytes();
        for (int j = 0; j < bytes.length; j++) {
            encbytes[j] = (byte) (bytes[j] ^ (byte) userId);
        }

        return Base64.getUrlEncoder().withoutPadding().encodeToString(encbytes);
    }
}