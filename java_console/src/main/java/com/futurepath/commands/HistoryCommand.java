package com.futurepath.commands;

import com.futurepath.repo.RunRepository;
import java.util.List;

public class HistoryCommand implements Command {
  private final RunRepository repo = new RunRepository();

  @Override public String key() { return "2"; }
  @Override public String description() { return "View History (last 10 runs from JDBC/SQLite)"; }

  @Override public void run() {
    List<String> rows = repo.lastResponses(10);
    if (rows.isEmpty()) {
      System.out.println("No history found (SQLite).");
      return;
    }
    System.out.println("\n--- HISTORY (created_at | response_json) ---");
    for (String r : rows) System.out.println(r);
  }
}
