package es.practica.firmas;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.nio.file.Path;

public final class DssLabDesktopApp {

    private final JTextField inputXml = new JTextField();
    private final JTextField outputXml = new JTextField();
    private final JTextField p12Path = new JTextField();
    private final JPasswordField p12Password = new JPasswordField();
    private final JTextField tspUrl = new JTextField();
    private final JTextField tspUser = new JTextField();
    private final JPasswordField tspPassword = new JPasswordField();
    private final JCheckBox enableTsp = new JCheckBox("Habilitar TSA (XAdES-T)");
    private final JTextArea logs = new JTextArea(10, 80);

    public static void launch() {
        SwingUtilities.invokeLater(() -> new DssLabDesktopApp().buildAndShow());
    }

    private void buildAndShow() {
        JFrame frame = new JFrame("DSS Lab - Firma XAdES");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel form = new JPanel(new GridLayout(0, 3, 8, 8));
        addFileRow(form, "XML entrada", inputXml, false);
        addFileRow(form, "XML salida", outputXml, true);
        addFileRow(form, "PKCS#12 (.p12)", p12Path, false);

        form.add(new JLabel("Password PKCS#12"));
        form.add(p12Password);
        form.add(new JLabel());

        form.add(enableTsp);
        form.add(new JLabel());
        form.add(new JLabel());

        form.add(new JLabel("TSA URL"));
        form.add(tspUrl);
        form.add(new JLabel());

        form.add(new JLabel("TSA usuario"));
        form.add(tspUser);
        form.add(new JLabel());

        form.add(new JLabel("TSA password"));
        form.add(tspPassword);
        form.add(new JLabel());

        JButton signButton = new JButton("Firmar (XAdES-B/T)");
        signButton.addActionListener(e -> sign());

        logs.setEditable(false);

        JPanel root = new JPanel(new BorderLayout(10, 10));
        root.add(form, BorderLayout.NORTH);
        root.add(signButton, BorderLayout.CENTER);
        root.add(new JScrollPane(logs), BorderLayout.SOUTH);

        frame.setContentPane(root);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        logs.append("UI Java lista. Completa campos y pulsa Firmar.\n");
    }

    private void addFileRow(JPanel form, String label, JTextField field, boolean saveDialog) {
        form.add(new JLabel(label));
        form.add(field);
        JButton browse = new JButton("...");
        browse.addActionListener(e -> chooseFile(field, saveDialog));
        form.add(browse);
    }

    private void chooseFile(JTextField target, boolean saveDialog) {
        JFileChooser chooser = new JFileChooser();
        int result = saveDialog ? chooser.showSaveDialog(null) : chooser.showOpenDialog(null);
        if (result == JFileChooser.APPROVE_OPTION) {
            target.setText(chooser.getSelectedFile().getAbsolutePath());
        }
    }

    private void sign() {
        try {
            String tsp = enableTsp.isSelected() ? tspUrl.getText().trim() : "";
            SigningConfig config = new SigningConfig(
                    Path.of(inputXml.getText().trim()),
                    Path.of(outputXml.getText().trim()),
                    Path.of(p12Path.getText().trim()),
                    new String(p12Password.getPassword()),
                    tsp,
                    tspUser.getText().trim(),
                    new String(tspPassword.getPassword())
            );

            new XadesBaselineBSigner().sign(config);
            String level = config.hasTsp() ? "XAdES-T" : "XAdES-B";
            logs.append("OK: Firma creada en " + config.outputXml() + " (" + level + ")\n");
            JOptionPane.showMessageDialog(null, "Firma completada: " + level);
        } catch (Exception exc) {
            logs.append("ERROR: " + exc.getMessage() + "\n");
            JOptionPane.showMessageDialog(null, exc.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
