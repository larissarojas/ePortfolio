package com.example.weighttrackingapp;

import android.app.AlertDialog;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.List;

public class WeightAdapter extends RecyclerView.Adapter<WeightAdapter.WeightViewHolder> {

    private final List<String> weightList;
    private final DatabaseHelper dbHelper;
    private final Context context;

    public WeightAdapter(Context context, List<String> weightList, DatabaseHelper dbHelper) {
        this.context = context;
        this.weightList = weightList;
        this.dbHelper = dbHelper;
    }

    @NonNull
    @Override
    public WeightViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_weight, parent, false);
        return new WeightViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull WeightViewHolder holder, int position) {
        String entry = weightList.get(position);
        holder.weightText.setText(entry);

        holder.buttonDelete.setOnClickListener(v -> {
            String[] parts = entry.split(" lbs on ");
            if (parts.length == 2) {
                double weight = Double.parseDouble(parts[0]);
                String date = parts[1];
                boolean deleted = dbHelper.deleteWeightEntry(weight, date);
                if (deleted) {
                    weightList.remove(position);
                    notifyItemRemoved(position);
                    Toast.makeText(context, "Entry deleted", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(context, "Failed to delete", Toast.LENGTH_SHORT).show();
                }
            }
        });

        holder.buttonEdit.setOnClickListener(v -> {
            AlertDialog.Builder builder = new AlertDialog.Builder(context);
            builder.setTitle("Edit Weight");

            final EditText input = new EditText(context);
            input.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
            input.setText(entry.split(" lbs on ")[0]);
            builder.setView(input);

            builder.setPositiveButton("Save", (dialog, which) -> {
                String newWeightStr = input.getText().toString();
                if (!newWeightStr.isEmpty()) {
                    double newWeight = Double.parseDouble(newWeightStr);
                    String[] parts = entry.split(" lbs on ");
                    if (parts.length == 2) {
                        double oldWeight = Double.parseDouble(parts[0]);
                        String date = parts[1];
                        boolean updated = dbHelper.updateWeightEntry(oldWeight, newWeight, date);
                        if (updated) {
                            weightList.set(position, newWeight + " lbs on " + date);
                            notifyItemChanged(position);
                            Toast.makeText(context, "Entry updated", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(context, "Failed to update", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            });

            builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
            builder.show();
        });
    }

    @Override
    public int getItemCount() {
        return weightList.size();
    }

    public static class WeightViewHolder extends RecyclerView.ViewHolder {
        TextView weightText;
        Button buttonDelete, buttonEdit;

        public WeightViewHolder(View itemView) {
            super(itemView);
            weightText = itemView.findViewById(R.id.textWeightEntry);
            buttonDelete = itemView.findViewById(R.id.buttonDelete);
            buttonEdit = itemView.findViewById(R.id.buttonEdit);
        }
    }
}
