package com.futurepath.registry;

import java.util.LinkedHashMap;
import java.util.Map;

import com.futurepath.commands.Command;
import com.futurepath.commands.AnalyzeCommand;
import com.futurepath.commands.HistoryCommand;

public class CommandRegistry {
  private final Map<String, Command> commands = new LinkedHashMap<>();

  public CommandRegistry() {
    register(new AnalyzeCommand());
    register(new HistoryCommand());
  }

  private void register(Command c) { commands.put(c.key(), c); }
  public Map<String, Command> all() { return commands; }
  public Command get(String key) { return commands.get(key); }
}
