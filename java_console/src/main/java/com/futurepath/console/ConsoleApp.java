package com.futurepath.console;

import java.util.Scanner;
import com.futurepath.registry.CommandRegistry;
import com.futurepath.commands.Command;

public class ConsoleApp {
  private final CommandRegistry registry = new CommandRegistry();
  private final MenuRenderer menu = new MenuRenderer();
  private final Scanner sc = new Scanner(System.in);

  public void start() {
    while (true) {
      menu.render(registry);
      System.out.print("Choose: ");
      String k = sc.nextLine().trim();
      if (k.equals("0")) return;

      Command cmd = registry.get(k);
      if (cmd == null) {
        System.out.println("Invalid option.");
        continue;
      }
      cmd.run();
    }
  }
}
