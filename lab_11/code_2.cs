using System;
using System.Text;

class Program
{
    static string alphabet = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя";
    static int alphabetSize = alphabet.Length;

    static int GetLetterIndex(char letter)
    {
        return alphabet.IndexOf(char.ToLower(letter));
    }

    static char ShiftLetter(char letter, int shift)
    {
        int index = GetLetterIndex(letter);
        if (index == -1) return letter;

        int newIndex = (index + shift) % alphabetSize;
        if (newIndex < 0) newIndex += alphabetSize;

        char shiftedLetter = alphabet[newIndex];
        return char.IsUpper(letter) ? char.ToUpper(shiftedLetter) : shiftedLetter;
    }

    static string Encrypt(string text, string key)
    {
        StringBuilder encryptedText = new StringBuilder();
        for (int i = 0; i < text.Length; i++)
        {
            int shift = GetLetterIndex(key[i % key.Length]);
            encryptedText.Append(ShiftLetter(text[i], shift));
        }
        return encryptedText.ToString();
    }

    static string Decrypt(string text, string key)
    {
        StringBuilder decryptedText = new StringBuilder();
        for (int i = 0; i < text.Length; i++)
        {
            int shift = GetLetterIndex(key[i % key.Length]);
            decryptedText.Append(ShiftLetter(text[i], -shift));
        }
        return decryptedText.ToString();
    }

    static void Main()
    {
        string text = "Муха Богдан";
        string key = "ключ";

        string encryptedText = Encrypt(text, key);
        Console.WriteLine("Зашифрований текст: " + encryptedText);

        string decryptedText = Decrypt(encryptedText, key);
        Console.WriteLine("Розшифрований текст: " + decryptedText);
        Console.WriteLine();
    }
}
