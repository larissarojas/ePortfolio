package com.example.weighttrackingapp;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class ProgressActivity extends AppCompatActivity {

    private EditText editTextWeight;
    private EditText editTextGoalWeight;
    private WeightAdapter adapter;
    private DatabaseHelper dbHelper;
    private List<String> weightEntries;
    private static final int SMS_PERMISSION_REQUEST_CODE = 101;
    private double userGoalWeight = -1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_progress);

        dbHelper = new DatabaseHelper(this);

        editTextWeight = findViewById(R.id.editTextWeight);
        editTextGoalWeight = findViewById(R.id.editTextGoalWeight);
        Button buttonAddWeight = findViewById(R.id.buttonAddWeight);
        Button buttonSmsPermission = findViewById(R.id.buttonSmsPermission);
        RecyclerView recyclerView = findViewById(R.id.recyclerViewWeights);

        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        weightEntries = dbHelper.getAllWeights();
        adapter = new WeightAdapter(this, weightEntries, dbHelper);
        recyclerView.setAdapter(adapter);

        buttonAddWeight.setOnClickListener(v -> {
            String weightText = editTextWeight.getText().toString();
            String goalText = editTextGoalWeight.getText().toString();

            if (!weightText.isEmpty()) {
                double weight = Double.parseDouble(weightText);

                if (!goalText.isEmpty()) {
                    userGoalWeight = Double.parseDouble(goalText);
                }

                boolean success = dbHelper.addWeightEntry(weight);
                if (success) {
                    Toast.makeText(this, getString(R.string.weight_added), Toast.LENGTH_SHORT).show();
                    editTextWeight.setText("");

                    String newEntry = dbHelper.getLastWeightEntry();
                    weightEntries.add(newEntry);
                    adapter.notifyItemInserted(weightEntries.size() - 1);

                    if (userGoalWeight > 0 && Math.abs(weight - userGoalWeight) < 0.01) {
                        sendGoalReachedSms();
                    }
                } else {
                    Toast.makeText(this, getString(R.string.error_saving_weight), Toast.LENGTH_SHORT).show();
                }
            } else {
                Toast.makeText(this, getString(R.string.enter_weight_prompt), Toast.LENGTH_SHORT).show();
            }
        });

        buttonSmsPermission.setOnClickListener(v -> {
            Intent intent = new Intent(ProgressActivity.this, SmsPermissionActivity.class);
            startActivity(intent);
        });
    }

    private void sendGoalReachedSms() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) == PackageManager.PERMISSION_GRANTED) {
            SmsManager smsManager = getSystemService(SmsManager.class);
            if (smsManager != null) {
                String phoneNumber = "+11234567890"; // Sample of phone number including country code
                String message = getString(R.string.goal_sms_text);
                smsManager.sendTextMessage(phoneNumber, null, message, null, null);
                Toast.makeText(this, getString(R.string.goal_sms_sent), Toast.LENGTH_SHORT).show();
            }
        } else {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.SEND_SMS}, SMS_PERMISSION_REQUEST_CODE);
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == SMS_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, getString(R.string.permission_granted), Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, getString(R.string.permission_denied), Toast.LENGTH_SHORT).show();
            }
        }
    }
}