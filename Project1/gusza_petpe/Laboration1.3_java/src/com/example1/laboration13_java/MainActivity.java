package com.example1.laboration13_java;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.Bundle;
import android.support.v4.view.GravityCompat;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.os.Build;
import android.widget.*;
import android.widget.RelativeLayout.LayoutParams;
import android.graphics.Color;
import android.widget.EditText;
import java.lang.Object;


public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
	  super.onCreate(savedInstanceState);

	  //myButton.setWidth(RelativeLayout.LayoutParams.WRAP_CONTENT);
	  
	  TextView textField1 = new TextView(this);
	  textField1.setText("Hur trivs du på LiU");
	  textField1.setGravity(Gravity.CENTER_HORIZONTAL);
	  TextView textField2 = new TextView(this);
	  textField2.setText("Läser du på LiTH");
	  textField2.setGravity(Gravity.CENTER_HORIZONTAL);
	  TextView textField3 = new TextView(this);
	  textField3.setText("Är detta LiUs logotyp");
	  textField3.setGravity(Gravity.CENTER_HORIZONTAL);
	  
	  CheckBox chBoxBra = new CheckBox(this);
	  chBoxBra.setText("Bra");
	  CheckBox chBoxMktBra = new CheckBox(this);
	  chBoxMktBra.setText("Mycket Bra");
	  CheckBox chBoxJBra = new CheckBox(this);
	  chBoxJBra.setText("Jättebra");
	  chBoxJBra.setChecked(true);
//	  textField1.setPadding(0, 10, 0, 0);
	  CheckBox chBoxJa = new CheckBox(this);
	  chBoxJa.setText("Ja");
	  CheckBox chBoxNej = new CheckBox(this);
	  chBoxNej.setText("Nej");
	  chBoxNej.setChecked(true);
	  CheckBox chBoxJa2 = new CheckBox(this);
	  chBoxJa.setText("Ja");
	  chBoxJa2.setChecked(true);
	  CheckBox chBoxNej2 = new CheckBox(this);
	  chBoxNej2.setText("Nej");
	  
	  ImageView imgView = new ImageView(this);
	  imgView.setImageResource(R.drawable.liu);


	  LinearLayout myLayout = new LinearLayout(this);
	  myLayout.setOrientation(LinearLayout.VERTICAL);
//	  	layoutHor.setWeightSum(1f);
	  myLayout.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
	  
	    
	  LinearLayout layoutCheckbox1 = new LinearLayout(this);
	  layoutCheckbox1.setOrientation(LinearLayout.HORIZONTAL);
//	  	layoutLeft.setWeightSum(0.25f);
	  layoutCheckbox1.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
	  
	  LinearLayout layoutCheckbox2 = new LinearLayout(this);
	  layoutCheckbox2.setOrientation(LinearLayout.HORIZONTAL);
//	  	layoutLeft.setWeightSum(0.25f);
	  layoutCheckbox2.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
	  	
	  LinearLayout layoutCheckbox3 = new LinearLayout(this);
	  layoutCheckbox3.setOrientation(LinearLayout.HORIZONTAL);
//	  	layoutLeft.setWeightSum(0.25f);
	  layoutCheckbox3.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
	  	
	  
	  
	  layoutCheckbox1.addView(chBoxBra);
	  layoutCheckbox1.addView(chBoxMktBra);
	  layoutCheckbox1.addView(chBoxJBra);
	  
	  layoutCheckbox2.addView(chBoxJa);
	  layoutCheckbox2.addView(chBoxNej);
	  
	  layoutCheckbox3.addView(chBoxJa2);
	  layoutCheckbox3.addView(chBoxNej2);
	  
      myLayout.addView(textField1);
      myLayout.addView(layoutCheckbox1);
      myLayout.addView(textField2);
      myLayout.addView(layoutCheckbox2);
      myLayout.addView(imgView);
      myLayout.addView(textField3);
      myLayout.addView(layoutCheckbox3);
      
      setContentView(myLayout);


	}

}