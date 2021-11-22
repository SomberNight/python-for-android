package org.kivy.android;

import android.os.SystemClock;

import java.io.InputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;


import android.view.ViewGroup;
import android.view.KeyEvent;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.util.Log;
import android.widget.Toast;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.PowerManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.widget.ImageView;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;

import android.widget.AbsoluteLayout;
import android.view.ViewGroup.LayoutParams;

import android.net.Uri;

import org.renpy.android.ResourceManager;

import org.kivy.android.launcher.Project;


import org.qtproject.qt5.android.bindings.QtActivity;

// Required by PythonService class
public class PythonActivity extends QtActivity {
    private static final String TAG = "PythonActivity";

    private ResourceManager resourceManager = null;
    public static PythonActivity mActivity = null;
    public static boolean mBrokenLibraries;
    protected static ViewGroup mLayout;

    // TODO: not functional currently
    public static native void nativeSetenv(String name, String value);

    public String getAppRoot() {
        String app_root =  getFilesDir().getAbsolutePath() + "/app";
        return app_root;
    }

    public String getEntryPoint(String search_dir) {
        /* Get the main file (.pyc|.pyo|.py) depending on if we
         * have a compiled version or not.
        */
        List<String> entryPoints = new ArrayList<String>();
        entryPoints.add("main.pyo");  // python 2 compiled files
        entryPoints.add("main.pyc");  // python 3 compiled files
        for (String value : entryPoints) {
            File mainFile = new File(search_dir + "/" + value);
            if (mainFile.exists()) {
                return value;
            }
        }
        return "main.py";
    }

    public static void initialize() {
        // The static nature of the singleton and Android quirkyness force us to initialize everything here
        // Otherwise, when exiting the app and returning to it, these variables *keep* their pre exit values
//         mWebView = null;
        mLayout = null;
        mBrokenLibraries = false;
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.v(TAG, "My oncreate running");
        resourceManager = new ResourceManager(this);

        this.mActivity = this;
//         this.showLoadingScreen();
        //new UnpackFilesTask().execute(getAppRoot());

        super.onCreate(savedInstanceState);
    }

    private class UnpackFilesTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {
            File app_root_file = new File(params[0]);
            Log.v(TAG, "Ready to unpack");
            PythonActivityUtil pythonActivityUtil = new PythonActivityUtil(mActivity, resourceManager);
            pythonActivityUtil.unpackData("private", app_root_file);
            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            Log.v("Python", "Device: " + android.os.Build.DEVICE);
            Log.v("Python", "Model: " + android.os.Build.MODEL);

            PythonActivity.initialize();

            String app_root_dir = getAppRoot();
            if (getIntent() != null && getIntent().getAction() != null &&
                    getIntent().getAction().equals("org.kivy.LAUNCH")) {
                File path = new File(getIntent().getData().getSchemeSpecificPart());

                Project p = Project.scanDirectory(path);
                String entry_point = getEntryPoint(p.dir);
                PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", p.dir + "/" + entry_point);
                PythonActivity.nativeSetenv("ANDROID_ARGUMENT", p.dir);
                PythonActivity.nativeSetenv("ANDROID_APP_PATH", p.dir);

                if (p != null) {
                    if (p.landscape) {
                        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
                    } else {
                        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
                    }
                }

                // Let old apps know they started.
                try {
                    FileWriter f = new FileWriter(new File(path, ".launch"));
                    f.write("started");
                    f.close();
                } catch (IOException e) {
                    // pass
                }
            } else {
                String entry_point = getEntryPoint(app_root_dir);
                PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", entry_point);
                PythonActivity.nativeSetenv("ANDROID_ARGUMENT", app_root_dir);
                PythonActivity.nativeSetenv("ANDROID_APP_PATH", app_root_dir);
            }

            String mFilesDirectory = mActivity.getFilesDir().getAbsolutePath();
            Log.v(TAG, "Setting env vars for start.c and Python to use");
            PythonActivity.nativeSetenv("ANDROID_PRIVATE", mFilesDirectory);
            PythonActivity.nativeSetenv("ANDROID_UNPACK", app_root_dir);
            PythonActivity.nativeSetenv("PYTHONHOME", app_root_dir);
            PythonActivity.nativeSetenv("PYTHONPATH", app_root_dir + ":" + app_root_dir + "/lib");
            PythonActivity.nativeSetenv("PYTHONOPTIMIZE", "2");

        }
    }

}

