const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });

  revealItems.forEach(item => observer.observe(item));
} else {
  revealItems.forEach(item => item.classList.add("is-visible"));
}

const channelSets = {
  uk: {
    smm: [["instagram", "Instagram"], ["tiktok", "TikTok"], ["telegram", "Telegram"], ["facebook", "Facebook"]],
    website: [["landing", "Лендінг"], ["corporate-site", "Корпоративний сайт"], ["portfolio", "Портфоліо"], ["booking", "Бронювання"]],
    content: [["reels", "Reels"], ["photo", "Фото"], ["copywriting", "Тексти"], ["creatives", "Креативи"]],
    ads: [["meta-ads", "Meta Ads"], ["google-ads", "Google Ads"], ["tiktok-ads", "TikTok Ads"], ["analytics", "Аналітика"]],
    branding: [["visual-identity", "Візуальний стиль"], ["tone-of-voice", "Tone of voice"], ["presentation", "Презентація"], ["brand-guide", "Brand guide"]],
    default: [["instagram", "Instagram"], ["tiktok", "TikTok"], ["telegram", "Telegram"], ["website", "Website"]]
  },
  en: {
    smm: [["instagram", "Instagram"], ["tiktok", "TikTok"], ["telegram", "Telegram"], ["facebook", "Facebook"]],
    website: [["landing", "Landing page"], ["corporate-site", "Corporate site"], ["portfolio", "Portfolio"], ["booking", "Booking flow"]],
    content: [["reels", "Reels"], ["photo", "Photo"], ["copywriting", "Copywriting"], ["creatives", "Ad creatives"]],
    ads: [["meta-ads", "Meta Ads"], ["google-ads", "Google Ads"], ["tiktok-ads", "TikTok Ads"], ["analytics", "Analytics"]],
    branding: [["visual-identity", "Visual identity"], ["tone-of-voice", "Tone of voice"], ["presentation", "Presentation"], ["brand-guide", "Brand guide"]],
    default: [["instagram", "Instagram"], ["tiktok", "TikTok"], ["telegram", "Telegram"], ["website", "Website"]]
  }
};

const categorySelect = document.querySelector('select[name="category"]');
const channelOptions = document.querySelectorAll("[data-channel-option]");

function updateChannelOptions() {
  const lang = document.documentElement.lang === "en" ? "en" : "uk";
  const selectedSet = channelSets[lang][categorySelect?.value] || channelSets[lang].default;

  channelOptions.forEach((label, index) => {
    const option = selectedSet[index];
    const input = label.querySelector("input");
    const text = label.querySelector("span");

    if (!option) {
      label.classList.add("is-hidden");
      input.checked = false;
      return;
    }

    label.classList.remove("is-hidden");
    input.value = option[0];
    input.checked = false;
    text.textContent = option[1];
  });
}

categorySelect?.addEventListener("change", updateChannelOptions);
window.addEventListener("languagechange", updateChannelOptions);
updateChannelOptions();
