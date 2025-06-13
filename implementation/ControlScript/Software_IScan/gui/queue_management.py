"""
Queue Management GUI Component
Contains operation queue display and control interface for the I-Scan application.
"""

import tkinter as tk
from tkinter import ttk


class QueueManagement:
    """GUI component for operation queue management"""
    
    def __init__(self, parent, callbacks=None, repeat_var=None):
        """
        Initialize queue management
        
        Args:
            parent: Parent widget
            callbacks: Dictionary containing callback functions
            repeat_var: BooleanVar for repeat queue option
        """
        self.parent = parent
        self.callbacks = callbacks or {}
        self.repeat_var = repeat_var
        
        self.frame = None
        self.queue_list = None
        self.queue_scrollbar = None
        
        # Button widgets
        self.queue_exec_btn = None
        self.queue_clear_btn = None
        self.queue_remove_btn = None
        self.queue_export_btn = None
        self.queue_import_btn = None
        self.repeat_check = None
        
    def create_frame(self):
        """Create the queue management frame and widgets"""
        self.frame = tk.LabelFrame(self.parent, text="Operationswarteschlange")
        self.frame.pack(fill="both", expand=True, padx=10, pady=2)
        
        # Queue list with scrollbar
        self.queue_list = tk.Listbox(self.frame, width=70, height=8)
        self.queue_list.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        self.queue_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.queue_list.yview)
        self.queue_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.queue_list.config(yscrollcommand=self.queue_scrollbar.set)
        
        # Buttons frame
        queue_buttons_frame = tk.Frame(self.frame)
        queue_buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=5, pady=5)
        
        # Create button rows
        self.create_button_rows(queue_buttons_frame)
        
        # Configure callbacks
        self.configure_callbacks()
        
        return self.frame
    
    def create_button_rows(self, parent):
        """Create button rows with organized layout"""
        # Row 1: Execute and Clear
        row1 = tk.Frame(parent)
        row1.pack(fill="x")
        
        self.queue_exec_btn = tk.Button(
            row1, 
            text="Warteschlange ausführen", 
            bg="#77dd77", 
            fg="black", 
            font=("Arial", 10, "bold")
        )
        self.queue_exec_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.queue_clear_btn = tk.Button(
            row1, 
            text="Warteschlange löschen",
            bg="#ff6961", 
            fg="black"
        )
        self.queue_clear_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Row 2: Remove and Repeat
        row2 = tk.Frame(parent)
        row2.pack(fill="x")
        
        self.queue_remove_btn = tk.Button(row2, text="Ausgewählte entfernen")
        self.queue_remove_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        if self.repeat_var:
            self.repeat_check = tk.Checkbutton(
                row2, 
                text="Warteschlange wiederholen", 
                variable=self.repeat_var
            )
            self.repeat_check.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Row 3: Import and Export
        row3 = tk.Frame(parent)
        row3.pack(fill="x")
        
        self.queue_export_btn = tk.Button(
            row3, 
            text="Warteschlange exportieren (CSV)", 
            bg="#b0c4de", 
            fg="black"
        )
        self.queue_export_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.queue_import_btn = tk.Button(
            row3, 
            text="Warteschlange importieren (CSV)", 
            bg="#b0c4de", 
            fg="black"
        )
        self.queue_import_btn.pack(side=tk.LEFT, padx=5, pady=2)
    
    def configure_callbacks(self):
        """Configure button callbacks"""
        if 'queue_exec' in self.callbacks:
            self.queue_exec_btn.config(command=self.callbacks['queue_exec'])
        if 'queue_clear' in self.callbacks:
            self.queue_clear_btn.config(command=self.callbacks['queue_clear'])
        if 'queue_remove' in self.callbacks:
            self.queue_remove_btn.config(command=self.callbacks['queue_remove'])
        if 'queue_export' in self.callbacks:
            self.queue_export_btn.config(command=self.callbacks['queue_export'])
        if 'queue_import' in self.callbacks:
            self.queue_import_btn.config(command=self.callbacks['queue_import'])
    
    def add_item(self, item_text):
        """Add item to queue list"""
        if self.queue_list:
            self.queue_list.insert(tk.END, item_text)
    
    def remove_selected(self):
        """Remove selected items from queue list"""
        if self.queue_list:
            selected = self.queue_list.curselection()
            for index in reversed(selected):  # Remove from end to avoid index issues
                self.queue_list.delete(index)
    
    def clear_queue(self):
        """Clear all items from queue list"""
        if self.queue_list:
            self.queue_list.delete(0, tk.END)
    
    def get_selected_indices(self):
        """Get indices of selected items"""
        return self.queue_list.curselection() if self.queue_list else []
    
    def get_all_items(self):
        """Get all items in the queue"""
        if self.queue_list:
            return [self.queue_list.get(i) for i in range(self.queue_list.size())]
        return []
    
    def set_items(self, items):
        """Set all items in the queue"""
        self.clear_queue()
        for item in items:
            self.add_item(item)
    
    def get_widgets(self):
        """Return dictionary of widgets for external access"""
        return {
            'frame': self.frame,
            'queue_list': self.queue_list,
            'queue_scrollbar': self.queue_scrollbar,
            'queue_exec_btn': self.queue_exec_btn,
            'queue_clear_btn': self.queue_clear_btn,
            'queue_remove_btn': self.queue_remove_btn,
            'queue_export_btn': self.queue_export_btn,
            'queue_import_btn': self.queue_import_btn,
            'repeat_check': self.repeat_check
        }
