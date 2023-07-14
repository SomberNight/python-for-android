package org.kivy.android;

import java.io.InputStream;
import java.io.File;

import android.app.Activity;
import android.util.Log;

import android.content.Context;
import android.content.pm.ActivityInfo;

import org.renpy.android.ResourceManager;

import org.kivy.android.launcher.Project;

import org.qtproject.qt.android.QtActivityDelegate;
import org.qtproject.qt.android.multimedia.QtMultimediaUtils;

/*
 * this class is added to android.app.static_init_classes metadata key.
 */
public class PythonActivityInit {
    private static final String TAG = "PythonActivityInit";

    private PythonActivity mActivity;
    private QtActivityDelegate mLoader;

    public void setActivity(Activity activity, Object o) {
        Log.v(TAG, "PythonActivityInit setActivity running");
        Log.v(TAG, activity.getClass().getName());
        mActivity = (PythonActivity)activity;
        Log.v(TAG, o.getClass().getName());
        mLoader = (QtActivityDelegate)o;

        // QtMultimediaUtils doesn't get initialized with the activity instance (?)
        // force it here.
        QtMultimediaUtils.setContext(mActivity);
    }

    public void setContext(Context context) {
        Log.v(TAG, "PythonActivityInit setContext running");
        Log.v(TAG, context.getClass().getName());

        Log.v(TAG, "activity env = " + mActivity.ENVIRONMENT_VARIABLES);

        String app_root_dir = mActivity.getAppRoot();

        Log.v(TAG, "Ready to unpack");
        PythonUtil.unpackAsset(mActivity, "private", new File(app_root_dir), true);
        PythonUtil.unpackPyBundle(mActivity, mActivity.getApplicationInfo().nativeLibraryDir + "/" + "libpybundle", new File(app_root_dir), false);
        Log.v(TAG, "Device: " + android.os.Build.DEVICE);
        Log.v(TAG, "Model: " + android.os.Build.MODEL);

        PythonActivity.initialize(); //Bundle extras = mActivity.getIntent().getExtras();

        if (mActivity.getIntent() != null && mActivity.getIntent().getAction() != null &&
                mActivity.getIntent().getAction().equals("org.kivy.LAUNCH")) {
            File path = new File(mActivity.getIntent().getData().getSchemeSpecificPart());

            Project p = Project.scanDirectory(path);
            String entry_point = mActivity.getEntryPoint(p.dir);
            PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", p.dir + "/" + entry_point);
            PythonActivity.nativeSetenv("ANDROID_ARGUMENT", p.dir);
            PythonActivity.nativeSetenv("ANDROID_APP_PATH", p.dir);

            if (p != null) {
                if (p.landscape) {
                    mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
                } else {
                    mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
                }
            }
        } else {
            String entry_point = mActivity.getEntryPoint(app_root_dir);
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

        Log.v(TAG, "Setting env vars for Qt");
        PythonActivity.nativeSetenv("QT_QUICK_CONTROLS_STYLE", "Material");
    }
}
