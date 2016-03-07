package com.example1.laboration12_java;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.Bundle;
import android.support.v4.view.GravityCompat;
import android.text.InputType;
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
	  Button myButton = new Button(this);
	  myButton.setText("KNAPP");
	  myButton.setWidth(600);
	  //myButton.setWidth(RelativeLayout.LayoutParams.WRAP_CONTENT);
	  
	  TextView textField1 = new TextView(this);
	  textField1.setText("Namn");
	  textField1.setPadding(0, 10, 0, 0);
	  
	  TextView textField2 = new TextView(this);
	  textField2.setText("Lösenord");
	  textField2.setPadding(0, 30, 0, 0);
	  
	  TextView textField3 = new TextView(this);
	  textField3.setText("Epost");
	  textField3.setPadding(0, 30, 0, 0);
	  
	  TextView textField4 = new TextView(this);
	  textField4.setText("Ålder");
	  textField4.setPadding(0, 30, 0, 0);
	  
	  EditText edtText1 = new EditText(this);
	  edtText1.setText("Anders");
	  
	  EditText edtText2 = new EditText(this);
	  edtText2.setText("•••••••");
	  edtText2.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
	  
	  EditText edtText3 = new EditText(this);
	  edtText3.setText("anders.froberg@liu.se");
//	  edtText3.setWidth(600);
	  
	  SeekBar skBar = new SeekBar(this);
	  skBar.setProgress(30);

	  LinearLayout layoutHor = new LinearLayout(this);
	  	layoutHor.setOrientation(LinearLayout.HORIZONTAL);
//	  	layoutHor.setWeightSum(1f);
	  	layoutHor.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
	  
	    
	  LinearLayout layoutLeft = new LinearLayout(this);
	  	layoutLeft.setOrientation(LinearLayout.VERTICAL);
//	  	layoutLeft.setWeightSum(0.25f);
	  	layoutLeft.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
	  	
      LinearLayout layoutRight = new LinearLayout(this);
      	layoutRight.setOrientation(LinearLayout.VERTICAL);
//      	layoutRight.setWeightSum(0.75f);
      	layoutRight.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
      
      	
      layoutHor.addView(layoutLeft);
      layoutHor.addView(layoutRight);
		   
      layoutLeft.addView(textField1);
      layoutLeft.addView(textField2);
      layoutLeft.addView(textField3);
      layoutLeft.addView(textField4);
      layoutRight.addView(edtText1);
      layoutRight.addView(edtText2);
      layoutRight.addView(edtText3);
      layoutRight.addView(skBar);
      
      setContentView(layoutHor);

       

	}

}