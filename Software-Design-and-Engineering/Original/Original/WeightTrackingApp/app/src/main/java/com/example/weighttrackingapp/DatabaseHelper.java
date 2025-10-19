package com.example.weighttrackingapp;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;
import java.util.List;

public class DatabaseHelper extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "WeightTracker.db";
    private static final int DATABASE_VERSION = 1;

    // Users table
    private static final String TABLE_USERS = "users";
    private static final String COL_ID = "id";
    private static final String COL_USERNAME = "username";
    private static final String COL_PASSWORD = "password";

    // Weights table
    private static final String TABLE_WEIGHTS = "weights";
    private static final String COL_WEIGHT_ID = "id";
    private static final String COL_WEIGHT = "weight";
    private static final String COL_DATE = "timestamp";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // Create users table
        String createUsersTable = "CREATE TABLE " + TABLE_USERS + " (" +
                COL_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COL_USERNAME + " TEXT UNIQUE, " +
                COL_PASSWORD + " TEXT)";
        db.execSQL(createUsersTable);

        // Create weights table
        String createWeightsTable = "CREATE TABLE " + TABLE_WEIGHTS + " (" +
                COL_WEIGHT_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COL_WEIGHT + " REAL, " +
                COL_DATE + " DATETIME DEFAULT CURRENT_TIMESTAMP)";
        db.execSQL(createWeightsTable);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USERS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_WEIGHTS);
        onCreate(db);
    }

    // Register new user
    public boolean registerUser(String username, String password) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COL_USERNAME, username);
        values.put(COL_PASSWORD, password);
        long result = db.insert(TABLE_USERS, null, values);
        return result != -1;
    }

    // Log in existing user
    public boolean loginUser(String username, String password) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(TABLE_USERS, null, COL_USERNAME + "=? AND " + COL_PASSWORD + "=?",
                new String[]{username, password}, null, null, null);
        boolean exists = (cursor.getCount() > 0);
        cursor.close();
        return exists;
    }

    // Add weight entry
    public boolean addWeightEntry(double weight) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COL_WEIGHT, weight);
        long result = db.insert(TABLE_WEIGHTS, null, values);
        return result != -1;
    }

    // Delete weight entry
    public boolean deleteWeightEntry(double weight, String date) {
        SQLiteDatabase db = this.getWritableDatabase();
        int result = db.delete(TABLE_WEIGHTS, COL_WEIGHT + "=? AND " + COL_DATE + "=?",
                new String[]{String.valueOf(weight), date});
        return result > 0;
    }

    // Update weight entry
    public boolean updateWeightEntry(double oldWeight, double newWeight, String date) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COL_WEIGHT, newWeight);
        int result = db.update(TABLE_WEIGHTS, values,
                COL_WEIGHT + "=? AND " + COL_DATE + "=?",
                new String[]{String.valueOf(oldWeight), date});
        return result > 0;
    }

    // Get all weight entries
    public List<String> getAllWeights() {
        List<String> weightList = new ArrayList<>();
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.rawQuery("SELECT * FROM " + TABLE_WEIGHTS + " ORDER BY " + COL_DATE + " DESC", null);
        if (cursor.moveToFirst()) {
            do {
                double weight = cursor.getDouble(cursor.getColumnIndexOrThrow(COL_WEIGHT));
                String date = cursor.getString(cursor.getColumnIndexOrThrow(COL_DATE));
                weightList.add(weight + " lbs on " + date);
            } while (cursor.moveToNext());
        }
        cursor.close();
        return weightList;
    }

    // Get the last weight entry (optional use)
    public String getLastWeightEntry() {
        List<String> allEntries = getAllWeights();
        return allEntries.isEmpty() ? "" : allEntries.get(0);
    }
}
