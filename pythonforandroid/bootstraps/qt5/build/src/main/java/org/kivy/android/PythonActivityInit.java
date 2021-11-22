package org.kivy.android;

import java.io.InputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.io.UnsupportedEncodingException;

import android.app.Activity;
import android.util.Log;
import android.util.Base64;

import android.content.Context;
import android.content.pm.ActivityInfo;

import org.renpy.android.ResourceManager;

import org.kivy.android.launcher.Project;

import org.qtproject.qt5.android.QtActivityDelegate;

/*
 * this class is added to android.app.static_init_classes metadata key
 * unfortunately it gets called before any loading of qt/other libs, so
 * we probably cannot do any library loading here
 */
public class PythonActivityInit {
    private static final String TAG = "PythonActivityInit";

    private PythonActivity mActivity;
    private QtActivityDelegate mLoader;

    public void setActivity(Activity activity, Object o) {
        Log.v(TAG, "PythonActivityInit setActivity running");

        //QtActivityDelegate delegate = (QtActivityDelegate)o;
        Log.v(TAG, activity.getClass().getName());
        mActivity = (PythonActivity)activity;
        Log.v(TAG, o.getClass().getName());
        mLoader = (QtActivityDelegate)o;
    }

    public void setContext(Context context) {
        Log.v(TAG, "PythonActivityInit setContext running");
        Log.v(TAG, context.getClass().getName());

        Log.v(TAG, "activity env = " + mActivity.ENVIRONMENT_VARIABLES);

        String app_root_dir = mActivity.getAppRoot();

        Log.v(TAG, "Ready to unpack");
        ResourceManager resourceManager = new ResourceManager(mActivity);
        PythonActivityUtil pythonActivityUtil = new PythonActivityUtil(mActivity, resourceManager);
        pythonActivityUtil.unpackData("private", new File(app_root_dir));



        Log.v(TAG, "Device: " + android.os.Build.DEVICE);
        Log.v(TAG, "Model: " + android.os.Build.MODEL);

        PythonActivity.initialize(); //Bundle extras = mActivity.getIntent().getExtras();

        HashMap<String,String> additionalEnv = new HashMap<>();

        if (mActivity.getIntent() != null && mActivity.getIntent().getAction() != null &&
                mActivity.getIntent().getAction().equals("org.kivy.LAUNCH")) {
            File path = new File(mActivity.getIntent().getData().getSchemeSpecificPart());

            Project p = Project.scanDirectory(path);
            String entry_point = mActivity.getEntryPoint(p.dir);
//             PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", p.dir + "/" + entry_point);
//             PythonActivity.nativeSetenv("ANDROID_ARGUMENT", p.dir);
//             PythonActivity.nativeSetenv("ANDROID_APP_PATH", p.dir);
            additionalEnv.put("ANDROID_ENTRYPOINT", p.dir + "/" + entry_point);
            additionalEnv.put("ANDROID_ARGUMENT", p.dir);
            additionalEnv.put("ANDROID_APP_PATH", p.dir);

            if (p != null) {
                if (p.landscape) {
                    mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
                } else {
                    mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
                }
            }

            // Let old apps know they started.
//             try {
//                 FileWriter f = new FileWriter(new File(path, ".launch"));
//                 f.write("started");
//                 f.close();
//             } catch (IOException e) {
//                 //pass
//             }
        } else {
            String entry_point = mActivity.getEntryPoint(app_root_dir);
//             PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", entry_point);
//             PythonActivity.nativeSetenv("ANDROID_ARGUMENT", app_root_dir);
//             PythonActivity.nativeSetenv("ANDROID_APP_PATH", app_root_dir);
            additionalEnv.put("ANDROID_ENTRYPOINT", entry_point);
            additionalEnv.put("ANDROID_ARGUMENT", app_root_dir);
            additionalEnv.put("ANDROID_APP_PATH", app_root_dir);
        }

        String mFilesDirectory = mActivity.getFilesDir().getAbsolutePath();
        Log.v(TAG, "Setting env vars for start.c and Python to use");
//         PythonActivity.nativeSetenv("ANDROID_PRIVATE", mFilesDirectory);
//         PythonActivity.nativeSetenv("ANDROID_UNPACK", app_root_dir);
//         PythonActivity.nativeSetenv("PYTHONHOME", app_root_dir);
//         PythonActivity.nativeSetenv("PYTHONPATH", app_root_dir + ":" + app_root_dir + "/lib");
//         PythonActivity.nativeSetenv("PYTHONOPTIMIZE", "2");

        additionalEnv.put("ANDROID_PRIVATE", mFilesDirectory);
        additionalEnv.put("ANDROID_UNPACK", app_root_dir);
        additionalEnv.put("PYTHONHOME", app_root_dir);
        additionalEnv.put("PYTHONPATH", app_root_dir + ":" + app_root_dir + "/lib");
        additionalEnv.put("PYTHONOPTIMIZE", "2");

        String combinedEnv = new String();
        for (String key: additionalEnv.keySet()) {
            combinedEnv += "\t" + key + "=" + additionalEnv.get(key);
        }
        try {
            byte[] env = combinedEnv.substring(1).getBytes("UTF-8");
            byte[] encodedEnv = Base64.encode(env, Base64.DEFAULT);

            mActivity.getIntent().putExtra("extraenvvars", new String(encodedEnv));

            Log.v(TAG, "Final Qt env: " + new String(encodedEnv));
        } catch (UnsupportedEncodingException e) {
            Log.v(TAG, "hmm");
        }

    }
}
