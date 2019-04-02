PASTEBIN_POST_LIST_RESPONSE = """
 <table class="maintable">
                        <tr>
                                <th scope="col">Name / Title</th>
                                <th scope="col" class="h_800 td_right">Posted</th>
                                <th scope="col" class="h_800 td_right">Syntax</th>
                        </tr>
                <tr>
                        <td><img src="/i/t.gif"  class="i_p0" alt="" /><a href="/3LzhZb3E">Untitled</a></td>
                        <td class="td_smaller h_800 td_right">2 sec ago</td>
                        <td class="td_smaller h_800 td_right">-</td>
                </tr>
                <tr>
                        <td><img src="/i/t.gif"  class="i_p0" alt="" /><a href="/5dTdTdez">Dsavhrgmk</a></td>
                        <td class="td_smaller h_800 td_right">27 sec ago</td>
                        <td class="td_smaller h_800 td_right">-</td>
                </tr>"""
PASTEBIN_POST_RESPONSE = """
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tampilan;
import java.sql.*;
import javax.swing.JOptionPane;
import javax.swing.table.DefaultTableModel;
import koneksi.koneksi;

/**
 *
 * @author Windows 7 Pro
 */
public class FormPasien extends javax.swing.JFrame {
    private Connection conn = new koneksi().connect();
    private DefaultTableModel tabmode;

    /**
     * Creates new form FormPasien
     */
    public FormPasien() {
        initComponents();
        datatable();
    }
    protected void aktif(){
        tnoidentitas.setEnabled(true);
        tnamapasien.setEnabled(true);
        talamat.setEnabled(true);
        tnoidentitas.requestFocus();               
    }
    protected void kosong(){
        tnoidentitas.setText("");
        tnamapasien.setText("");
        talamat.setText("");
        rlakilaki.setSelected(true);
        cgoldar.setSelectedIndex(0);
        tkatakuncipencarian.setText("");
    }
"""
GITHUB_POST_LIST_RESPONSE = [
    {'id': '99f98a7346faa9e86a4e3e34778eccb8',
    'description': '',
    'html_url': 'https://gist.github.com/99f98a7346faa9e86a4e3e34778eccb8',
     'files': {'example.js': {'raw_url': 'https://gist.githubusercontent.com/philipkueng/99f98a7346faa9e86a4e3e34778eccb8/raw/51d069b218b1cdc80f726992ac1ce3866f9d60ae/example.js',}}
     },
    {'id': '99f98a7346faa9e86a4e3e34778eccb8',
    'description': '',
    'html_url': 'https://gist.github.com/99f98a7346faa9e86a4e3e34778eccb8',
     'files': {'example.js': {'raw_url': 'https://gist.githubusercontent.com/philipkueng/99f98a7346faa9e86a4e3e34778eccb8/raw/51d069b218b1cdc80f726992ac1ce3866f9d60ae/example.js',}}
     },
    {'id': '99f98a7346faa9e86a4e3e34778eccb8',
    'description': '',
    'html_url': 'https://gist.github.com/99f98a7346faa9e86a4e3e34778eccb8',
     'files': {'example.js': {'raw_url': 'https://gist.githubusercontent.com/philipkueng/99f98a7346faa9e86a4e3e34778eccb8/raw/51d069b218b1cdc80f726992ac1ce3866f9d60ae/example.js',}}
     }
]

GITHUB_POST_RESPONSE = {
    "hello_world.rb": {
      "filename": "hello_world.rb",
      "type": "application/x-ruby",
      "language": "Ruby",
      "raw_url": "https://gist.githubusercontent.com/octocat/6cad326836d38bd3a7ae/raw/db9c55113504e46fa076e7df3a04ce592e2e86d8/hello_world.rb",
      "size": 167,
      "truncated": False,
      "content": "class HelloWorld\n   def initialize(name)\n      @name = name.capitalize\n   end\n   def sayHi\n      puts \"Hello !\"\n   end\nend\n\nhello = HelloWorld.new(\"World\")\nhello.sayHi"
    },
    "hello_world.py": {
      "filename": "hello_world.py",
      "type": "application/x-python",
      "language": "Python",
      "raw_url": "https://gist.githubusercontent.com/octocat/e29f3839074953e1cc2934867fa5f2d2/raw/99c1bf3a345505c2e6195198d5f8c36267de570b/hello_world.py",
      "size": 199,
      "truncated": False,
      "content": "class HelloWorld:\n\n    def __init__(self, name):\n        self.name = name.capitalize()\n       \n    def sayHi(self):\n        print \"Hello \" + self.name + \"!\"\n\nhello = HelloWorld(\"world\")\nhello.sayHi()"
    },
    "hello_world_ruby.txt": {
      "filename": "hello_world_ruby.txt",
      "type": "text/plain",
      "language": "Text",
      "raw_url": "https://gist.githubusercontent.com/octocat/e29f3839074953e1cc2934867fa5f2d2/raw/9e4544db60e01a261aac098592b11333704e9082/hello_world_ruby.txt",
      "size": 46,
      "truncated": False,
      "content": "Run `ruby hello_world.rb` to print Hello World"
    },
    "hello_world_python.txt": {
      "filename": "hello_world_python.txt",
      "type": "text/plain",
      "language": "Text",
      "raw_url": "https://gist.githubusercontent.com/octocat/e29f3839074953e1cc2934867fa5f2d2/raw/076b4b78c10c9b7e1e0b73ffb99631bfc948de3b/hello_world_python.txt",
      "size": 48,
      "truncated": False,
      "content": "Run `python hello_world.py` to print Hello World"
    }
}