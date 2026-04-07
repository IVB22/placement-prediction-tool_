package com.futurepath.db;

import com.futurepath.config.AppConfig;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public final class Db {
  private Db() {}

  public static Connection connect() {
    try {
      Connection c = DriverManager.getConnection(AppConfig.DB_URL);
      init(c);
      return c;
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private static void init(Connection c) {
    try (Statement st = c.createStatement()) {
      st.executeUpdate(
        "CREATE TABLE IF NOT EXISTS runs (" +
        "id INTEGER PRIMARY KEY AUTOINCREMENT," +
        "created_at TEXT NOT NULL," +
        "request_json TEXT NOT NULL," +
        "response_json TEXT NOT NULL" +
        ")"
      );
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
