package com.futurepath.config;

public final class AppConfig {
  private AppConfig() {}

  public static final String ML_BASE_URL = "http://127.0.0.1:5000";
  public static final String MATCH_PATH  = "/match-json";

  public static final String DB_URL = "jdbc:sqlite:futurepath.db";
}
