import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.File;

// Compilar Tree.java: javac -cp json-20240303.jar Tree.java

public class Tree {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {

            String filepath = "analisis_sintactico" + File.separator + "tree.json";

            // Leer el archivo JSON
            JSONObject jsonObject = readJsonFile(filepath);
            if (jsonObject == null) {
                System.out.println("Error al leer el archivo JSON");
                return;
            }

            // Crear el nodo raíz del árbol
            DefaultMutableTreeNode root = new DefaultMutableTreeNode(" ");

            // Construir el árbol desde el objeto JSON
            // buildTreeFromJsonArray(jsonObject.getJSONObject("main"), root);
            buildTreeFromJsonArray(jsonObject.getJSONArray("main"), root);

            // Crear el modelo de árbol
            DefaultTreeModel treeModel = new DefaultTreeModel(root);

            // Crear el JTree con el modelo de árbol
            JTree tree = new JTree(treeModel);

            // Expandir todos los nodos del árbol
            expandAllNodes(tree, 0, tree.getRowCount());

            // Crear y configurar la ventana
            JFrame frame = new JFrame("Arbol Sintactico");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new JScrollPane(tree));
            frame.setSize(800, 600);
            frame.setVisible(true);
        });
    }

    // Leer el archivo JSON y parsearlo
    private static JSONObject readJsonFile(String fileName) {
        try (FileInputStream fis = new FileInputStream(fileName)) {
            return new JSONObject(new JSONTokener(fis));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    // Construir el árbol desde el array JSON
    private static void buildTreeFromJsonArray(JSONArray jsonArray, DefaultMutableTreeNode parent) {
        for (int i = 0; i < jsonArray.length(); i++) {
            JSONObject jsonChild = jsonArray.getJSONObject(i);
            DefaultMutableTreeNode childNode = new DefaultMutableTreeNode(jsonChild.getString("name"));
            parent.add(childNode);
            if (jsonChild.has("children")) {
                buildTreeFromJsonArray(jsonChild.getJSONArray("children"), childNode);
            }
            if (jsonChild.has("siblings")) {
                buildTreeFromJsonArray(jsonChild.getJSONArray("siblings"), childNode);
            }
        }
    }

    // Método para expandir todos los nodos del árbol
    private static void expandAllNodes(JTree tree, int startingIndex, int rowCount) {
        for (int i = startingIndex; i < rowCount; ++i) {
            tree.expandRow(i);
        }

        if (tree.getRowCount() != rowCount) {
            expandAllNodes(tree, rowCount, tree.getRowCount());
        }
    }
}
