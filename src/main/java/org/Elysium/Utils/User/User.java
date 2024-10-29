package org.Elysium.Utils.User;

import org.Elysium.Utils.Inventory.Weapons.Claymore;
import org.Elysium.Utils.Inventory.Weapons.Sword;
import org.bson.Document;
import org.Elysium.Utils.Inventory.Weapons.Weapon;

import java.util.ArrayList;
import java.util.List;

public class User {
    private final String userId;
    private String username;
    private String currentRegion;
    private String elementalAffinity;
    private int experiencePoints;
    private long coins;
    private List<Weapon> weaponInventory;
    private List<String> consumableInventory; // Add consumable inventory

    public User(String userId, String username, String currentRegion, String elementalAffinity, int experiencePoints, long coins) {
        this.userId = userId;
        this.username = username;
        this.currentRegion = currentRegion;
        this.elementalAffinity = elementalAffinity;
        this.experiencePoints = experiencePoints;
        this.coins = coins;
        this.weaponInventory = new ArrayList<>();
        this.consumableInventory = new ArrayList<>(); // Initialize consumable inventory
    }

    public Document toDocument() {
        Document doc = new Document("user_id", userId)
                .append("username", username)
                .append("current_region", currentRegion)
                .append("elemental_affinity", elementalAffinity)
                .append("experience_points", experiencePoints)
                .append("coins", coins);

        // Only add inventories if they're not empty
        if (!weaponInventory.isEmpty()) {
            doc.append("weapon_inventory", inventoryToDocument(weaponInventory));
        }
        if (!consumableInventory.isEmpty()) {
            doc.append("consumable_inventory", consumableInventory);
        }

        return doc;
    }

    public static User fromDocument(Document doc) {
        User user = new User(
                doc.getString("user_id"),
                doc.getString("username"),
                doc.getString("current_region"),
                doc.getString("elemental_affinity"),
                doc.getInteger("experience_points"),
                doc.getLong("coins")
        );

        if (doc.containsKey("weapon_inventory")) {
            user.weaponInventory = documentToWeaponInventory(doc.get("weapon_inventory", List.class));
        }
        if (doc.containsKey("consumable_inventory")) {
            user.consumableInventory = new ArrayList<>(doc.getList("consumable_inventory", String.class));
        }

        return user;
    }

    private List<Document> inventoryToDocument(List<Weapon> inventory) {
        List<Document> weaponDocs = new ArrayList<>();
        for (Weapon weapon : inventory) {
            weaponDocs.add(new Document("item_id", weapon.getItemId())
                    .append("name", weapon.getName())
                    .append("region_origin", weapon.getRegionOrigin())
                    .append("type", weapon.getType())
                    .append("damage", weapon.getDamage())
                    .append("level", weapon.getLevel()));
        }
        return weaponDocs;
    }

    private static List<Weapon> documentToWeaponInventory(List<Document> docs) {
        List<Weapon> weapons = new ArrayList<>();
        for (Document doc : docs) {
            String type = doc.getString("type");
            Weapon weapon;
            if ("Sword".equals(type)) {
                weapon = new Sword(doc.getString("item_id"), doc.getString("name"), doc.getString("region_origin"));
            } else if ("Claymore".equals(type)) {
                weapon = new Claymore(doc.getString("item_id"), doc.getString("name"), doc.getString("region_origin"));
            } else {
                continue; // Skip unknown types
            }
            weapons.add(weapon);
        }
        return weapons;
    }

    public void addWeapon(Weapon weapon) {
        if (weapon == null) {
            throw new IllegalArgumentException("Cannot add a null weapon.");
        }
        weaponInventory.add(weapon);
    }

    public void removeWeapon(Weapon weapon) {
        if (weapon == null) {
            throw new IllegalArgumentException("Cannot remove a null weapon.");
        }
        if (!weaponInventory.remove(weapon)) {
            throw new IllegalArgumentException("Weapon not found in inventory.");
        }
    }

    public void addConsumable(String consumable) {
        if (consumable == null || consumable.isEmpty()) {
            throw new IllegalArgumentException("Cannot add a null or empty consumable.");
        }
        consumableInventory.add(consumable);
    }

    public void removeConsumable(String consumable) {
        if (consumable == null || consumable.isEmpty()) {
            throw new IllegalArgumentException("Cannot remove a null or empty consumable.");
        }
        if (!consumableInventory.remove(consumable)) {
            throw new IllegalArgumentException("Consumable not found in inventory.");
        }
    }

    public List<Weapon> getWeaponInventory() {
        return weaponInventory;
    }

    public List<String> getConsumableInventory() {
        return consumableInventory;
    }

    public String getUserId() {
        return userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getCurrentRegion() {
        return currentRegion;
    }

    public void setCurrentRegion(String currentRegion) {
        this.currentRegion = currentRegion;
    }

    public String getElementalAffinity() {
        return elementalAffinity;
    }

    public void setElementalAffinity(String elementalAffinity) {
        this.elementalAffinity = elementalAffinity;
    }

    public int getExperiencePoints() {
        return experiencePoints;
    }

    public void setExperiencePoints(int experiencePoints) {
        this.experiencePoints = experiencePoints;
    }

    public long getCoins() {
        return coins;
    }

    public void setCoins(long coins) {
        this.coins = coins;
    }
}
