package com.futurepath.console;

import com.futurepath.registry.CommandRegistry;
import com.futurepath.commands.Command;

public class MenuRenderer {
  public void render(CommandRegistry reg) {
    System.out.println("\n=== FuturePath (Java Console) ===");
    for (Command c : reg.all().values()) {
      System.out.println(c.key() + ") " + c.description());
    }
    System.out.println("0) Exit");
  }
}
