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

import org.renpy.android.ResourceManager;


import org.qtproject.qt.android.bindings.QtActivity;

public class PythonActivity extends QtActivity {
    private static final String TAG = "PythonActivity";

    private ResourceManager resourceManager = null;
    public static PythonActivity mActivity = null;
    public static boolean mBrokenLibraries;
    protected static ViewGroup mLayout;

    public static native void nativeSetenv(String name, String value);

    private static PythonActivityInit init = null;

    static {
        Log.v(TAG, "PythonActivity static");
        init = new PythonActivityInit();
    }

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
        init.setActivity(this, this);
        init.setContext(this);

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
                    // The below forces a redraw of the window/view, which is needed on some phones
                    // to actually clear the flag. However on some other phones, it crashes the app...
                    // see https://github.com/spesmilo/electrum/issues/8522
                    /*if (window.getDecorView().isAttachedToWindow()) {
                        WindowManager wm = this.mActivity.getWindowManager();
                        wm.removeViewImmediate(window.getDecorView());
                        wm.addView(window.getDecorView(), window.getAttributes());
                    }*/
                }
            }
        }._initialize(this, secure));
    }

    /**
     * Used by android.permissions p4a module to register a call back after
     * requesting runtime permissions
     **/
    public interface PermissionsCallback {
        void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults);
    }

    private PermissionsCallback permissionCallback;
    private boolean havePermissionsCallback = false;

    public void addPermissionsCallback(PermissionsCallback callback) {
        permissionCallback = callback;
        havePermissionsCallback = true;
        Log.v(TAG, "addPermissionsCallback(): Added callback for onRequestPermissionsResult");
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        Log.v(TAG, "onRequestPermissionsResult()");
        if (havePermissionsCallback) {
            Log.v(TAG, "onRequestPermissionsResult passed to callback");
            permissionCallback.onRequestPermissionsResult(requestCode, permissions, grantResults);
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    /**
     * Used by android.permissions p4a module to check a permission
     **/
    public boolean checkCurrentPermission(String permission) {
        if (android.os.Build.VERSION.SDK_INT < 23)
            return true;

        try {
            java.lang.reflect.Method methodCheckPermission =
                Activity.class.getMethod("checkSelfPermission", String.class);
            Object resultObj = methodCheckPermission.invoke(this, permission);
            int result = Integer.parseInt(resultObj.toString());
            if (result == PackageManager.PERMISSION_GRANTED)
                return true;
        } catch (IllegalAccessException | NoSuchMethodException |
                 InvocationTargetException e) {
        }
        return false;
    }

    /**
     * Used by android.permissions p4a module to request runtime permissions
     **/
    public void requestPermissionsWithRequestCode(String[] permissions, int requestCode) {
        if (android.os.Build.VERSION.SDK_INT < 23)
            return;
        try {
            java.lang.reflect.Method methodRequestPermission =
                Activity.class.getMethod("requestPermissions",
                String[].class, int.class);
            methodRequestPermission.invoke(this, permissions, requestCode);
        } catch (IllegalAccessException | NoSuchMethodException |
                 InvocationTargetException e) {
        }
    }

    public void requestPermissions(String[] permissions) {
        requestPermissionsWithRequestCode(permissions, 1);
    }


    //----------------------------------------------------------------------------
    // Listener interface for onNewIntent
    //

    public interface NewIntentListener {
        void onNewIntent(Intent intent);
    }

    private List<NewIntentListener> newIntentListeners = null;

    public void registerNewIntentListener(NewIntentListener listener) {
        if (this.newIntentListeners == null)
            this.newIntentListeners = new ArrayList<NewIntentListener>();
        synchronized (this.newIntentListeners) {
            this.newIntentListeners.add(listener);
        }
    }

    public void unregisterNewIntentListener(NewIntentListener listener) {
        if (this.newIntentListeners == null)
            return;
        synchronized (this.newIntentListeners) {
            this.newIntentListeners.remove(listener);
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        if (this.newIntentListeners == null)
            return;
        synchronized (this.newIntentListeners) {
            Iterator<NewIntentListener> iterator = this.newIntentListeners.iterator();
            while (iterator.hasNext()) {
                (iterator.next()).onNewIntent(intent);
            }
        }
    }

    //----------------------------------------------------------------------------
    // Listener interface for onActivityResult
    //

    public interface ActivityResultListener {
        void onActivityResult(int requestCode, int resultCode, Intent data);
    }

    private List<ActivityResultListener> activityResultListeners = null;

    public void registerActivityResultListener(ActivityResultListener listener) {
        if (this.activityResultListeners == null)
            this.activityResultListeners = new ArrayList<ActivityResultListener>();
        synchronized (this.activityResultListeners) {
            this.activityResultListeners.add(listener);
        }
    }

    public void unregisterActivityResultListener(ActivityResultListener listener) {
        if (this.activityResultListeners == null)
            return;
        synchronized (this.activityResultListeners) {
            this.activityResultListeners.remove(listener);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (this.activityResultListeners == null)
            return;
        // this.onResume();
        synchronized (this.activityResultListeners) {
            Iterator<ActivityResultListener> iterator = this.activityResultListeners.iterator();
            while (iterator.hasNext())
                (iterator.next()).onActivityResult(requestCode, resultCode, intent);
        }
    }

}
