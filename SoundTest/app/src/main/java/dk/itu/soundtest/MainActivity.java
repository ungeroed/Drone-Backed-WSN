package dk.itu.soundtest;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.media.AudioFormat;
import android.media.MediaRecorder;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.media.AudioRecord;
import android.widget.Toast;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;


public class MainActivity extends ActionBarActivity {

    private String FILENAME = "log";

    private TextView sound;
    private ListView logList;
    private EditText distance;
    private Button logButton;

    int BufferSize = 8820; // want to play 2048 (2K) since 2 bytes we use only 1024
    int BytesPerElement = 2; // 2 bytes in 16bit format

    private ArrayList<String> log;
    private ArrayAdapter<String> logAdapter;

    private Thread display;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        log = Load();
        sound = (TextView) findViewById(R.id.sound);
        logList = (ListView) findViewById(R.id.logList);
        distance = (EditText) findViewById(R.id.distance);
        logButton = (Button) findViewById(R.id.button);

        logAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, log);
        logList.setAdapter(logAdapter);

        createDisplay();
    }

    @Override
    protected void onDestroy(){
        super.onDestroy();
        display.interrupt();
        try {
            display.join();
        }catch(Exception e){}
    }

    private double soundPressureLevel(short[] data){
        double rmsValue = 0.0;

        for (int i = 0; i < data.length; i++) {
            rmsValue += data[i] * data[i];
        }
        rmsValue = rmsValue / (double) data.length;
        rmsValue = Math.sqrt(rmsValue);

        double splValue = 20 * Math.log10(rmsValue / 0.000002);
        splValue = Math.round(splValue * 100.0) / 100.0;
        return splValue;
    }

    public void logEntry(View v){
        final AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.MIC, 44100, AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT, BufferSize * BytesPerElement);
        final String dist = distance.getText().toString();
        distance.setText("");
        logButton.setEnabled(false);

        display.interrupt();
        try {
            display.join();
        }catch(Exception e){
            throw new RuntimeException(e);
        }

        new Thread(new Runnable() {
            @Override
            public void run() {
                record.startRecording();

                for(int i = 0; i < 50; i++) {
                    final short[] data = new short[BufferSize];
                    record.read(data, 0, BufferSize);

                    final double spl = soundPressureLevel(data);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            sound.setText("Sound Pressure Level: " + spl);
                            log.add(dist + " " + spl);
                            logAdapter.notifyDataSetChanged();
                            Save(log);
                        }
                    });
                }
                record.stop();

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        createDisplay();
                        CharSequence text = "Done!";
                        int duration = Toast.LENGTH_SHORT;

                        Toast toast = Toast.makeText(getApplicationContext(), text, duration);
                        toast.show();
                        logButton.setEnabled(true);
                    }
                });
            }
        }).start();
    }

    public void clearEntries(View v){
        log.clear();
        deleteFile(FILENAME);
        logAdapter.notifyDataSetChanged();
    }

    public void copy(View v){
        StringBuilder sb = new StringBuilder();

        ClipboardManager clipboard = (ClipboardManager)getSystemService(CLIPBOARD_SERVICE);

        for(String s : log){
            sb.append(s + "\n");
        }

        ClipData clipData = ClipData.newPlainText("text", sb.toString());
        clipboard.setPrimaryClip(clipData);
    }

    private void Save(ArrayList<String> data){
        try {
            FileOutputStream fos = openFileOutput(FILENAME, Context.MODE_PRIVATE);
            ObjectOutputStream out = new ObjectOutputStream(fos);
            out.writeObject(data);
            out.close();
            fos.close();
        }catch(Exception e){
            throw new RuntimeException(e);
        }
    }

    private ArrayList<String> Load(){
        try {
            FileInputStream fis = openFileInput(FILENAME);
            ObjectInputStream in = new ObjectInputStream(fis);
            return (ArrayList<String>) in.readObject();
        }catch(FileNotFoundException e){
            return new ArrayList<>();
        }catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private void createDisplay(){
        final AudioRecord record = new AudioRecord(MediaRecorder.AudioSource.MIC, 44100, AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT, BufferSize * BytesPerElement);

        display = new Thread(new Runnable() {
            @Override
            public void run() {
                record.startRecording();

                while(true && !Thread.currentThread().interrupted()) {
                    final short[] data = new short[BufferSize];
                    record.read(data, 0, BufferSize);

                    final double spl = soundPressureLevel(data);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            sound.setText("Sound Pressure Level: " + spl);
                        }
                    });
                }
                record.stop();
            }
        });
        display.start();

    }

}
