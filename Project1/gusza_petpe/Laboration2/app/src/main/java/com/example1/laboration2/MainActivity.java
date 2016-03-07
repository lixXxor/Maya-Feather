package com.example1.laboration2;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import android.graphics.Color;
import android.view.View;
import android.widget.ExpandableListView;
import android.widget.ExpandableListView.OnChildClickListener;
import android.widget.ExpandableListView.OnGroupClickListener;
import android.text.TextWatcher;
import android.text.Editable;


public class MainActivity extends ActionBarActivity {
	
    ExpandableListAdapter listAdapter;
    public static ExpandableListView expView;
    EditText edtText;
    List<String> listHeader;
    HashMap<String, List<String>> listChild;
    List<String> listDirectory;
    int currentExpanded;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
                
        expView = (ExpandableListView) findViewById(R.id.expandable_list);
        edtText = (EditText) findViewById(R.id.text_field);
        //edtText.setText("€/€");
        currentExpanded = -1;
        prepareListData();
        listDirectory = new ArrayList<String>();
        listAdapter = new ExpandableListAdapter(this, listHeader, listChild);
        
        expView.setAdapter(listAdapter);
        
        
        /**
         * The ongroupclicklistener checks if we click on the same group twice
         * or another group, and acts thereafter. This invokes the onTextChanged method
         * in edtText.
         * */
        expView.setOnGroupClickListener(new OnGroupClickListener() {
            @Override
            public boolean onGroupClick(ExpandableListView parent, View v, int groupPosition, long id) {
                if (currentExpanded == groupPosition){
                    if (!listDirectory.isEmpty()){
                        listDirectory.clear();
                    }
                    edtText.setText("");
                }
                else {
                    if(currentExpanded != -1) {
                        expView.collapseGroup(currentExpanded);
                    }
                    if (!listDirectory.isEmpty()){
                        listDirectory.clear();
                    }
                    edtText.setText(listHeader.get(groupPosition) + "/"+"€");
                }
                expView.setItemChecked(expView.getCheckedItemPosition(), false);

                return true;
            }
        });

        expView.setOnChildClickListener(new OnChildClickListener() {

            @Override
            public boolean onChildClick(ExpandableListView parent, View v,
                    int groupPosition, int childPosition, long id) {
            	edtText.setText(listHeader.get(groupPosition) 
            			+ "/" 
            			+ listChild.get(listHeader.get(groupPosition)).get(childPosition)
            			+ "€");
                int index = expView.getFlatListPosition(ExpandableListView.getPackedPositionForChild(groupPosition, childPosition));

                expView.setItemChecked(index, true);
                edtText.setBackgroundColor(Color.TRANSPARENT);
                return false;
            }
        });



        
        // Search in edtbar
        edtText.addTextChangedListener(new TextWatcher() {

            @Override
            public void onTextChanged(CharSequence cs, int start, int before, int count) {

            }

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count,
                    int after) {
            }

            @Override
            public void afterTextChanged(Editable s) {
        		String text = edtText.getText().toString().toLowerCase(Locale.getDefault()).replace("/€", "");
        		//If listDirectory is empty, we should search for a match!
                if(listDirectory.isEmpty()){
                	listDirectory.add(text);
	                if(listHeader.contains(listDirectory.get(0))){
	                	expView.expandGroup(listHeader.indexOf(text));
	                	currentExpanded = listHeader.indexOf(text);
	                }
	                else if(currentExpanded != -1){
	                	expView.collapseGroup(currentExpanded);
	                	listDirectory.clear();
	                	currentExpanded = -1;
	                }
	                else{
	                	listDirectory.clear();
	                }
                    //Check if listHeader contains any of the input words
                    if(containsSequence(listHeader, text)){
                        edtText.setBackgroundColor(Color.TRANSPARENT);
                    }
                    else{
                        edtText.setBackgroundColor(Color.RED);
                    }
                }
                //There is something in listDirectory
                else{
                    //Changed from string to charsequence of the child.
                	CharSequence child = text.replace(listDirectory.get(0)+"/", "");

                	if(text.contains(listDirectory.get(0))){
	                	if(containsSequence(listChild.get(listHeader.get(currentExpanded)), child)){
	                		edtText.setBackgroundColor(Color.TRANSPARENT);
                            expView.setItemChecked(expView.getCheckedItemPosition(), false);
                            if(listChild.get(listHeader.get(currentExpanded)).contains(child)) {
                                int index = expView.getFlatListPosition(ExpandableListView
                                        .getPackedPositionForChild(currentExpanded, listChild.
                                                get(listHeader.get(currentExpanded)).indexOf(child)));
                                expView.setItemChecked(index, true);
                            }
	                	}
	                	else{
                            expView.setItemChecked(expView.getCheckedItemPosition(), false);
	                		edtText.setBackgroundColor(Color.RED);
	                	}
	                		
	                }
                	else if(currentExpanded != -1){
 	                	expView.collapseGroup(currentExpanded);
 	                	listDirectory.clear();
 	                	edtText.setBackgroundColor(Color.RED);
 	                	currentExpanded = -1;
 	                }
                	else{
                		edtText.setBackgroundColor(Color.RED);
                	}
            	}
            }

        });

    }

    private void prepareListData() {
        listHeader = new ArrayList<String>();
        listChild = new HashMap<String, List<String>>();
 
        // Adding header data
        listHeader.add("light");
        listHeader.add("medium");
        listHeader.add("dark");
        listHeader.add("dark");

        // Adding child data
        List<String> color = new ArrayList<String>();
        color.add("green");
        color.add("yellow");
        color.add("red");
        color.add("blue");

        List<String> color_2 = new ArrayList<>();
        color_2.add("blue");

        // Adding to list
        listChild.put(listHeader.get(0), color); // Header, Child data
        listChild.put(listHeader.get(1), color);
        listChild.put(listHeader.get(2), color);
        listChild.put(listHeader.get(3), color_2);
    }

    /**
     * containsSequence checks an arraylist if it contains a charsequence
     * The .contains of List in java checks .equals for each object, we wish to check for the
     * String.contains(CharSequence) instead. This checks and returns true/false if a sequence is contained
     * in any of the list elements.
     * **/
    public boolean containsSequence(List<String> arrlist, CharSequence cs){
        for(int i = 0; i<arrlist.size(); i++){
            if(arrlist!=null && arrlist.get(i).contains(cs)){
                return true;
            }
        }
        return false;
    }

    public static ExpandableListView getExpView(){
        return expView;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
