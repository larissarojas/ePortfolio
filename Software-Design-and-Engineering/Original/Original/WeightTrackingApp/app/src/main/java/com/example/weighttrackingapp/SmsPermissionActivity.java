package com.example.weighttrackingapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class SmsPermissionActivity extends AppCompatActivity {

    private static final int REQUEST_SMS_PERMISSION = 101;
    private TextView textPermissionStatus;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sms_permission);

        textPermissionStatus = findViewById(R.id.textPermissionStatus);
        Button buttonRequestPermission = findViewById(R.id.buttonRequestSmsPermission);

        // Check permission on load
        updatePermissionStatus();

        // Button to request permission
        buttonRequestPermission.setOnClickListener(v -> {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.SEND_SMS},
                        REQUEST_SMS_PERMISSION);
            } else {
                textPermissionStatus.setText(getString(R.string.permission_already_granted));
            }
        });
    }

    private void updatePermissionStatus() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS)
                == PackageManager.PERMISSION_GRANTED) {
            textPermissionStatus.setText(getString(R.string.permission_already_granted));
        } else {
            textPermissionStatus.setText(getString(R.string.permission_not_granted));
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_SMS_PERMISSION) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                textPermissionStatus.setText(getString(R.string.permission_granted));
            } else {
                textPermissionStatus.setText(getString(R.string.permission_denied));
            }
        }
    }
}