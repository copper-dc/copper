package org.Elysium.Elysium.Norax;

import org.bson.Document;

import java.util.List;

public class Region {
    public String regionId;
    public String name;
    public String elementalPower;
    public String description;
    public List<Document> quests;

    public Region(String regionId, String name, String elementalPower, String description, List<Document> quests) {
        this.regionId = regionId;
        this.name = name;
        this.elementalPower = elementalPower;
        this.description = description;
        this.quests = quests;
    }

    public Document toDocument() {
        return new Document("region_id", regionId)
                .append("name", name)
                .append("elemental_power", elementalPower)
                .append("description", description)
                .append("quests", quests);
    }

    public static Region fromDocument(Document doc) {
        return new Region(
                doc.getString("region_id"),
                doc.getString("name"),
                doc.getString("elemental_power"),
                doc.getString("description"),
                (List<Document>) doc.get("quests")
        );
    }

    public String getRegionId() {
        return regionId;
    }

    public void setRegionId(String regionId) {
        this.regionId = regionId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getElementalPower() {
        return elementalPower;
    }

    public void setElementalPower(String elementalPower) {
        this.elementalPower = elementalPower;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<Document> getQuests() {
        return quests;
    }

    public void setQuests(List<Document> quests) {
        this.quests = quests;
    }
}
