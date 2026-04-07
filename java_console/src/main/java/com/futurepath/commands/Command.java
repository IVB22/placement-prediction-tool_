package com.futurepath.commands;
public interface Command {
  String key();
  String description();
  void run();
}
