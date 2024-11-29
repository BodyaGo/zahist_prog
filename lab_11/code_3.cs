using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        string inputText = "Муха Богдан";
        Dictionary<char, char> encryptionTable = CreateEncryptionTable();
        Dictionary<char, char> decryptionTable = CreateDecryptionTable(encryptionTable);

        string encryptedText = Encrypt(inputText, encryptionTable);
        string decryptedText = Decrypt(encryptedText, decryptionTable);

        Console.WriteLine($"Оригінальний текст: {inputText}");
        Console.WriteLine($"Зашифрований текст: {encryptedText}");
        Console.WriteLine($"Розшифрований текст: {decryptedText}");
        Console.WriteLine();
    }

    static Dictionary<char, char> CreateEncryptionTable()
    {
        return new Dictionary<char, char>
        {
            {'А', 'Л'}, {'Б', 'В'}, {'В', 'Г'}, {'Г', 'Д'}, {'Ґ', 'Е'}, {'Д', 'Ж'},
            {'Е', 'З'}, {'Є', 'И'}, {'Ж', 'Й'}, {'З', 'К'}, {'И', 'М'}, {'Й', 'Н'},
            {'К', 'О'}, {'Л', 'П'}, {'М', 'Р'}, {'Н', 'С'}, {'О', 'Т'}, {'П', 'У'},
            {'Р', 'Ф'}, {'С', 'Х'}, {'Т', 'Ц'}, {'У', 'Ч'}, {'Ф', 'Ш'}, {'Х', 'Щ'},
            {'Ц', 'Ь'}, {'Ч', 'Ю'}, {'Ш', 'Я'}, {'Щ', 'А'}, {'Ь', 'Б'}, {'Ю', 'В'},
            {'Я', 'Г'}, {'І', 'Ґ'}, {'Ї', 'Д'}, {'_', '_'}, {' ', ' '},

            {'а', 'л'}, {'б', 'в'}, {'в', 'г'}, {'г', 'д'}, {'ґ', 'е'}, {'д', 'ж'},
            {'е', 'з'}, {'є', 'и'}, {'ж', 'й'}, {'з', 'к'}, {'и', 'м'}, {'й', 'н'},
            {'к', 'о'}, {'л', 'п'}, {'м', 'р'}, {'н', 'с'}, {'о', 'т'}, {'п', 'у'},
            {'р', 'ф'}, {'с', 'х'}, {'т', 'ц'}, {'у', 'ч'}, {'ф', 'ш'}, {'х', 'щ'},
            {'ц', 'ь'}, {'ч', 'ю'}, {'ш', 'я'}, {'щ', 'а'}, {'ь', 'б'}, {'ю', 'в'},
            {'я', 'г'}, {'і', 'ґ'}, {'ї', 'д'}
        };
    }

    static Dictionary<char, char> CreateDecryptionTable(Dictionary<char, char> encryptionTable)
    {
        Dictionary<char, char> decryptionTable = new Dictionary<char, char>();
        foreach (var pair in encryptionTable)
        {
            decryptionTable[pair.Value] = pair.Key;
        }
        return decryptionTable;
    }

    static string Encrypt(string text, Dictionary<char, char> table)
    {
        char[] encryptedChars = new char[text.Length];
        for (int i = 0; i < text.Length; i++)
        {
            encryptedChars[i] = table.ContainsKey(text[i]) ? table[text[i]] : text[i];
        }
        return new string(encryptedChars);
    }

    static string Decrypt(string text, Dictionary<char, char> table)
    {
        char[] decryptedChars = new char[text.Length];
        for (int i = 0; i < text.Length; i++)
        {
            decryptedChars[i] = table.ContainsKey(text[i]) ? table[text[i]] : text[i];
        }
        return new string(decryptedChars);
    }
}