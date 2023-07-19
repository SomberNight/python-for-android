package org.kivy.android;

import android.os.SystemClock;

import java.io.InputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.Runnable;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;


import android.view.ViewGroup;
import android.view.KeyEvent;
import android.view.Window;
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
import android.view.WindowManager;

import android.net.Uri;

import androidx.core.view.ViewCompat;

import org.renpy.android.ResourceManager;

import org.kivy.android.launcher.Project;


import org.qtproject.qt.android.bindings.QtActivity;

public class PythonActivity extends QtActivity {
    private static final String TAG = "PythonActivity";

    private ResourceManager resourceManager = null;
    public static PythonActivity mActivity = null;
    public static boolean mBrokenLibraries;
    protected static ViewGroup mLayout;

    public static native void nativeSetenv(String name, String value);

    public String getAppRoot() {
        return getFilesDir().getAbsolutePath() + "/app";
    }

    public String getEntryPoint(String search_dir) {
        /* Get the main file (.pyc|.py) depending on if we
         * have a compiled version or not.
         */
        File mainFile = new File(search_dir + "/main.pyc");
        if (mainFile.exists()) {
            return "main.pyc";
        }
        return "main.py";
    }

    public static void initialize() {
        // The static nature of the singleton and Android quirkyness force us to initialize everything here
        // Otherwise, when exiting the app and returning to it, these variables *keep* their pre exit values
        mLayout = null;
        mBrokenLibraries = false;
    }

    private void loadNativeLib() {
        Log.v(TAG, "loading native lib");
        try {
            System.loadLibrary("main");
        } catch (java.lang.UnsatisfiedLinkError e) {
            // alternate library load, some Android 5 devices fail
            // the above loadLibrary call.
            Log.v(TAG, "loading native lib (alt)");
            String libPath = this.getFilesDir().getParentFile().getAbsolutePath() + "/lib";
            System.load(libPath + "/libmain.so");
        }
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.v(TAG, "My onCreate running");
        resourceManager = new ResourceManager(this);

        this.mActivity = this;

        loadNativeLib();

        super.onCreate(savedInstanceState);
    }

    public void setSecureWindow(boolean secure) {
        runOnUiThread(new Runnable() {
            private Activity mActivity;
            private boolean mEnable;

            public Runnable _initialize(Activity activity, boolean enable) {
                this.mActivity = activity;
                this.mEnable = enable;
                return this;
            }

            @Override
            public void run() {
                Window window = this.mActivity.getWindow();

                if ( !((window.getAttributes().flags & WindowManager.LayoutParams.FLAG_SECURE) != 0) ^ mEnable)
                    return; // no change needed

                if (mEnable) {
                    Log.v(TAG, "Setting Secure Window");
                    window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE);
                } else {
                    Log.v(TAG, "UnSetting Secure Window");
                    window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE);
                    if (ViewCompat.isAttachedToWindow(window.getDecorView())) {
                        WindowManager wm = this.mActivity.getWindowManager();
                        wm.removeViewImmediate(window.getDecorView());
                        wm.addView(window.getDecorView(), window.getAttributes());
                    }
                }
            }
        }._initialize(this, secure));
    }

    //----------------------------------------------------------------------------
    // Listener interface for onNewIntent
    //

    public interface NewIntentListener {
        void onNewIntent(Intent intent);
    }

    private List<NewIntentListener> newIntentListeners = null;

    public void registerNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            this.newIntentListeners = Collections.synchronizedList(new ArrayList<NewIntentListener>());
        this.newIntentListeners.add(listener);
    }

    public void unregisterNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            return;
        this.newIntentListeners.remove(listener);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        if ( this.newIntentListeners == null )
            return;
        this.onResume();
        synchronized ( this.newIntentListeners ) {
            Iterator<NewIntentListener> iterator = this.newIntentListeners.iterator();
            while ( iterator.hasNext() ) {
                (iterator.next()).onNewIntent(intent);
            }
        }
    }

}
