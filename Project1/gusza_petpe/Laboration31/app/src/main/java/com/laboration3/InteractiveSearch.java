package com.laboration3;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.text.Editable;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListPopupWindow;
import android.text.TextWatcher;
import android.widget.ListView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Locale;

/**
 * Created by Mike on 2014-12-10.
 *
 */
public class InteractiveSearch extends EditText {
    //URL
    private static String url = "http://flask-afteach.rhcloud.com/getnames/";
    private static String sendURL = url;

    //JSON Node Names
    private static final String TAG_ID = "id";
    private static final String TAG_RESULT = "result";
    // List view
    ListView lv;
    ListPopupWindow lstPopWindow;
    int currentId;
    // Listview Adapter
    public static ArrayAdapter<String> adapter;

    //JSON ArrayNames
    JSONArray ResultJSON;

    // ArrayList for Listview
    ArrayList<String> resultList;
    Activity activity;
    //Required super-constructors
    public InteractiveSearch(Context context, AttributeSet attrs){
        super(context, attrs);
        init(context);
    }
    public InteractiveSearch(Context context){
        super(context);
        init(context);
    }
    public InteractiveSearch(Context context, AttributeSet attrs, int defStyle){
        super(context, attrs, defStyle);
        init(context);
    }

    //Crashes in init
    private void init(Context context){
        this.activity = (Activity) context;
        activity.setContentView(R.layout.activity_main);
        Log.d("tag", context.toString());

        resultList = new ArrayList<String>();
        adapter = new ArrayAdapter<String>(activity, R.layout.list_item, R.id.child_name, resultList);
        //Listview can't get a contentview like this... then how?
        lv = (ListView) activity.findViewById(R.id.list_view);
        Log.d("tag", lv.toString());
        lstPopWindow = new ListPopupWindow(this.activity);
        lstPopWindow.setAnchorView(lv);
        this.addTextChangedListener(new TextWatcher() {
            @Override
            public void onTextChanged (CharSequence s,int start, int before, int count){
                // TODO Auto-generated method stub

                adapter.getFilter().filter(s);
            }

            @Override
            public void beforeTextChanged (CharSequence s,int start, int count,
                                           int after){
                // TODO Auto-generated method stub

            }

            @Override
            public void afterTextChanged (Editable s){
                // TODO Auto-generated method stub

                String text = s.toString().toLowerCase(Locale.getDefault());
                currentId++;
                sendURL = url + currentId + "/" + text;
                new GetContacts().execute();

                Log.d("HEJMIKPE", " dettaskanogsynaskanskeinte" +sendURL);

            }
        });
    }



    /**
     * Async task class to get json by making HTTP call
     * */

     private class GetContacts extends AsyncTask<Void, Void, Void> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected Void doInBackground(Void... arg0) {
            // Creating service handler class instance
            ServiceHandler sh = new ServiceHandler();

            // Making a request to url and getting response
            String jsonStr = sh.makeServiceCall(sendURL, ServiceHandler.GET);

            Log.d("HEJMIKPE", "> " + jsonStr);

            if (jsonStr != null) {
                try {
                    JSONObject jsonObj = new JSONObject(jsonStr);
                    Log.d("HEJMIKPE", "> " + jsonStr);
                    // Getting JSON Array node
                    // {"id": "3", "result": ["EMMA", "EMMALINE", "EMMIE", "EMMY"]} format
                    int id = Integer.parseInt(jsonObj.getString(TAG_ID));
                    if(id==currentId){

                        resultList.clear();

                        ResultJSON = jsonObj.getJSONArray(TAG_RESULT);

                        // looping through All Names
                        for (int i = 0; i < ResultJSON.length(); i++) {

                            String c = ResultJSON.getString(i);



                            resultList.add(c);
                        }

                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } else {
                Log.e("ServiceHandler", "Couldn't get any data from the url");
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);

            /**
             * Updating parsed JSON data into ListView
             * */
            Log.d("HEJMIKPE", " hittt" + resultList.size());

            adapter = new ArrayAdapter<String>(getContext(), R.layout.list_item, R.id.child_name, resultList);

            adapter.sort(new Comparator<String>() {
                public int compare(String object1, String object2) {
                    return object1.compareTo(object2);
                };
            });
            Log.d("HEJMIKPE", " asdjkjkadskjldsakljsadkljasc" + resultList.size());

            lstPopWindow.setAdapter(adapter);
            lstPopWindow.show();
            //lv.setAdapter(adapter);

            adapter.notifyDataSetChanged();
            Log.d("HEJMIKPE", " laststuff" + resultList.size());

        }

    }

}
