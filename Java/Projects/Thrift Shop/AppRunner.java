/**
 * AppRunner implements Runnable to bootstrap the Thrift Shop application
 * on the Swing Event Dispatch Thread (EDT).
 * 
 * Using a dedicated top-level class prevents the generation of anonymous
 * inner classes (e.g., Thriftshop$1.class).
 */
public class AppRunner implements Runnable {
    @Override
    public void run() {
        new Thriftshop();
    }
}
