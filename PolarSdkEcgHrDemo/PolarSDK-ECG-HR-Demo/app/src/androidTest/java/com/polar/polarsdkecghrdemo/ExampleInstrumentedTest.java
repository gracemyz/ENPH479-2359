package com.polar.polarsdkecghrdemo;

import static androidx.test.core.app.ApplicationProvider.getApplicationContext;

import android.content.Context;
//import androidx.test.core;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Instrumented test, which will execute on an Android device.
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedTest {
    @Test
    public void useAppContext() {
        // Context of the app under test.
        Context appContext = getApplicationContext();

        assertEquals("com.polar.polarsdkdemo", appContext.getPackageName());
    }
}
